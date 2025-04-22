import time
import requests

# Global variables
DPID = 4 # central switch ID
PORT_TO_GWI = 5 # port to GWI
THRESHOLD = 1200 # threshold for latency
CHECK_INTERVAL = 2 # interval to check the system state

adaptation_done = False # flag to indicate if adaptation is done
# MAPE loop functions

def monitor():
    """
    Monitor function to collect numbers of paquets transmitted to GWI.
    """
    try:
        stats= requests.get(f"http://localhost:8080/stats/port/{DPID}/{PORT_TO_GWI}").json()
        for port_stats in stats[str(DPID)]:
            if port_stats['port_no'] == PORT_TO_GWI:
                return port_stats.get('tx_packets', 0) # return the number of transmitted packets
    except requests.RequestException as e:
        print("Error fetching stats:", e)
        return 0
    except ValueError as e: 
        print("Error parsing JSON response:", e)
        return 0
    except KeyError as e:
        print("Key error in response:", e)
        return 0
    except Exception as e:
        print("An unexpected error occurred:", e)
        return 0

def analyze(current_packets):
    """
    Analyze function to process collected data.
    """
    print(f"[Analyzing...] Total packets transmitted to GWI: {current_packets}")
    return current_packets > THRESHOLD

def plan():
    """
    Plan function to determine necessary actions.
    """
    print("[Planning...] Overload detected, Preparing to redirect to GI2.")

def execute():
    """
    Execute function to apply the planned actions.
    """
    print("[Executing actions...] Redirecting traffic to GI2 via ofctl_rest.")
    redirection_rule = {
        "dpid": DPID,
        "priority": 100,
        "match": {
            "in_port": 1 # port connected to Zone 1
        },
        "actions": [
            {
                "type": "OUTPUT",
                "port": 4 # port connected to GI2
            }
        ]
    }
    try:
        response = requests.post("http://localhost:8080/stats/flowentry/add", json=redirection_rule)
        # print("[DEBUG] Raw Response Content:", response.text)  # Log raw response
        print("HTTP request successful:", response.status_code)
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    # """
    # Main function to run the MAPE loop.
    # """
    while True:
        current_tx = monitor()
        if not adaptation_done and analyze(current_tx):
            plan()
            execute()
            adaptation_done = True
        else:
            print("[Stable Network; No adaptation needed ...]")
        time.sleep(CHECK_INTERVAL) # Wait for the specified interval before the next loop
    # execute()