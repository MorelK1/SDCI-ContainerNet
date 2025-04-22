import time
import requests

# Global variables
DPID = 231930737332042 # central switch ID
PORT_TO_GWI = 5 # port to GWI
THRESHOLD = 10000 # threshold for latency
CHECK_INTERVAL = 2 # interval to check the system state
# MAPE loop functions

def monitor():
    """
    Monitor function to collect numbers of paquets transmitted to GWI.
    """
    try:
        stats= requests.get(f"http://localhost:8080/stats/port/{DPID}/{PORT_TO_GWI}").json()
        return stats['tx_packets']
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

def analyze():
    """
    Analyze function to process collected data.
    """
    print("Analyzing data...")
    # Example: Simulate data analysis
    time.sleep(1)

def plan():
    """
    Plan function to determine necessary actions.
    """
    print("Planning actions...")
    # Example: Simulate planning
    time.sleep(1)

def execute():
    """
    Execute function to apply the planned actions.
    """
    print("Executing actions...")
    # Example: Simulate an HTTP request
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        if response.status_code == 200:
            print("HTTP request successful:", response.json())
        else:
            print("HTTP request failed with status code:", response.status_code)
    except requests.RequestException as e:
        print("HTTP request error:", e)

def main():
    """
    Main function to run the MAPE loop.
    """
    while True:
        monitor()
        analyze()
        plan()
        execute()
        time.sleep(CHECK_INTERVAL)  # Wait for the specified interval before the next loop

if __name__ == "__main__":
    main()