import time
import requests
from subprocess import Popen

# Configuration
GWI_HEALTH_URL = "http://localhost:8181/health"
OVERLOAD_THRESHOLD = 70 # seuil de surchage CPU (%)
CHECK_INTERVAL = 2 # secondes entre chaque verification

# Containers
LAUNCH_GI2 = (
    "docker exec gi2 node gateway.js " \
    "--local_ip 10.0.0.12 --local_port 8182 " \
    "--local_name gi2 --remote_ip 10.0.0.1 " \
    "--remote_port 8080 --remote_name srv &"
)

REDIRECT_GF1 = (
    "docker exec gf1 pkill node && " \
    "docker exec gf1 node gateway.js " \
    "--local_ip 10.0.0.3 --local_port 8281 " \
    "--local_name gf1 --remote_ip 10.0.0.11 " \
    "remote_port 8182 --remote_name gi2 &"
)

adaptation_done = False

while True:
    try:
        response = requests.get(GWI_HEALTH_URL, timeout=1)
        data = response.json()
        # print(data)
        load = data["currentLoad"]
        print(f"Current load on gwi: {load:.2f}%")

        if load > OVERLOAD_THRESHOLD and not adaptation_done:
            print("\n[; INCIDENT] Durchage detectee sur gwi. Lancement de l'adaptation")
            print ("[+] Lancement de gi2...")
            Popen(LAUNCH_GI2, shell= True)
            time.sleep(1)
            print("[+] Redemarrage de gf1 vers gi2...")
            Popen(REDIRECT_GF1, shell=True)

        elif load <= OVERLOAD_THRESHOLD:
            print("Gwi en charge normale")
            adaptation_done = True

    except Exception as e:
        print(f"[Erreur] Impossible de recuperer /health: {e}")
    
    time.sleep(CHECK_INTERVAL)