import requests
import json
import os
import time
import sys
import subprocess

sys.path.append(os.path.abspath(".."))

from env_config import ENV_CONFIG

with open("../mac.json") as f:
    data = json.load(f)
GWI_MAC = data["gwi"]
GF1_MAC = data["gf1"]
NEW_VNF_MAC = None

monitoring = True
delay_monitoring = 5

# Demmarage de la VNF de monitoring
def start_monitoring():
    url = "http://127.0.0.1:5001/restapi/compute/dc1/monitor"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "image": "sdci_monitor",
        "network": "(id=monitor,ip=10.0.0.20/24)",
        # "params": {
        #     "TARGET_URL": "http://10.0.0.2:8181/health",
        #     "MONITOR_HOST": "10.0.0.20",
        #     "MONITOR_PORT": "5000"
        # }
    }

    response = requests.put(url, headers=headers, data=json.dumps(payload))
    return response.status_code, response.json()

def get_monitoring_data():
    result = subprocess.check_output(["docker", "exec", "mn.monitor", "curl", "http://localhost:5000/monitor"])
    rd = json.loads(result.decode())
    # print(rd)
    return rd["status"], rd["data"]



# Creation d'une nouvelle GW intermédiaire
def create_intermediate_gw():
    global NEW_VNF_MAC
    url = "http://127.0.0.1:5001/restapi/compute/dc1/gi2"

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "image": "sdci-gw-vnf",
        "network": "(id=vnf_gi2,ip=10.0.0.12/24)",
        "properties": {"env": ENV_CONFIG["gi2"]}
    }
    print(json.dumps(payload, indent=2))
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    # if response.status_code == 200:
    #     data = response.json()
    #     # Enregistrement de l'adresse MAC de la nouvelle GW intermédiaire
    #     network_info = data.get("network", [])
    #     if network_info:
    #         NEW_VNF_MAC = network_info[0].get("mac")
    #     print("✅ VNF 'sdci_gateway' déployée avec succès.")
    #     print("Réponse :", response.json())
    #     # return new_vnf_mac
    # else:
    #     print(f"❌ Échec du déploiement (code {response.status_code})")
    #     print("Détail :", response.text)
    return response.status_code, response.json()

def redirect_forward():
    global GWI_MAC
    global GF1_MAC
    global NEW_VNF_MAC

    # Define the flow entry payload
    redirection_rule = {
        "dpid": 4,
        "priority": 100,
        "match": {
            "in_port": 1, # port d'entrée de gf1 vers s4
            "ipv4_src": "10.0.0.3", # ip du conteneur gf1
            "ipv4_dst": "10.0.0.2", # ip de gwi
            "eth_type": 2048,
            "ip_proto": 6
        },
        "actions": [
            {
                "type": "SET_FIELD",
                "field": "ipv4_dst",
                "value": "10.0.0.12"
            },
            {
                "type": "SET_FIELD",
                "field": "eth_dst",
                "value": NEW_VNF_MAC
            },
            { "type": "SET_FIELD", "field": "tcp_dst", "value": 8182 },
            {
                "type": "OUTPUT",
                "port": 5
            }
        ]
    }

    headers = {'Content-Type': 'text/plain'}
    payload = str(redirection_rule)

    # Send the POST request
    try:
        response = requests.post("http://localhost:8080/stats/flowentry/add", data=payload, headers=headers)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
    except requests.RequestException as e:
        print("Error sending POST request:", e)

def redirect_backward():
    global GWI_MAC
    global GF1_MAC
    global NEW_VNF_MAC

    reverse_rule = {
        "dpid": 4,
        "priority": 100,
        "match": {
            "eth_type": 2048,
            "ip_proto": 6,
            "ipv4_src": "10.0.0.12",   # gi2
            "ipv4_dst": "10.0.0.3"     # gf1
        },
        "actions": [
            {
                "type": "SET_FIELD",
                "field": "ipv4_src",
                "value": "10.0.0.2"     # masquerading pour faire croire à gf1 que c’est gwi
            },
            {
                "type": "SET_FIELD",
                "field": "eth_src",
                "value": GWI_MAC
            },
            {
                "type": "SET_FIELD",
                "field": "tcp_src",
                "value": 8181
            },
            {
                "type": "OUTPUT",
                "port": 1
            }
        ]
    }
    # Send the POST request
    try:
        response = requests.post("http://localhost:8080/stats/flowentry/add", json=reverse_rule)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
    except requests.RequestException as e:
        print("Error sending POST request:", e)

def redirect():
    redirect_forward()
    redirect_backward()
    print("Redirection rules applied.")



if __name__ == "__main__":
    single_gwi = True
    # Demarrage de la VNF de monitoring
    status_code, response = start_monitoring()
    while status_code != 200:
        try:
            time.sleep(delay_monitoring)
            status_code, response = start_monitoring()
        except:
            print("Error during monitoring startup")
            time.sleep(delay_monitoring)
            continue
    print("Monitoring VNF started successfully.")
    monitoring = True

    while monitoring:
        time.sleep(delay_monitoring)
        try:
            status, data = get_monitoring_data()
            # print("Monitoring data:", monitoring_data)
            if status != "OK":
                raise Exception("Monitoring data not OK")
            
            else:
                # gettraffic info
                avgLoad = data["avgLoad"]
                currentLoadSystem = data["currentLoadSystem"]
                currentLoad = data["currentLoad"]

                if currentLoadSystem >  5:
                    traffic_issue = True
                else:
                    traffic_issue = False
                
                if traffic_issue and single_gwi:
                    
                    print("Traffic issue detected. Current load:", currentLoadSystem)
                    try:
                        # Demarrage de la nouvelle GW intermédiaire
                        new_vnf_code, new_vnf_data = create_intermediate_gw()

                        if new_vnf_code == 200:
                            print("New GWI created successfully.")
                            # Enregistrement de l'adresse MAC de la nouvelle GW intermédiaire
                            network_info = new_vnf_data.get("network", [])
                            if network_info:
                                NEW_VNF_MAC = network_info[0].get("mac")
                            print("New VNF MAC:", NEW_VNF_MAC)
                            # Redirection du trafic

                            redirect()
                            single_gwi = False
                            continue
                        
                    except Exception as e:
                        print("Error during redirection:", e)
                        monitoring = False
                else:
                    print("No traffic issue detected.")
        except Exception as e:
            print("Error during monitoring:", e)
            monitoring = False
            # Optionally, you can stop the monitoring VNF here
            # stop_monitoring()














    # c,r = get_monitoring_data()

    # print(c)
    # print("----------------------------------------")
    # print(r)





    

    
