ENV_CONFIG = {
    "srv": {
        "LOCAL_IP": "10.0.0.1",
        "LOCAL_PORT": "8080",
        "LOCAL_NAME": "srv"
    },
    "gwi": {
        "LOCAL_IP": "10.0.0.2",
        "LOCAL_PORT": "8181",
        "LOCAL_NAME": "gwi",
        "REMOTE_IP": "10.0.0.1",
        "REMOTE_PORT": "8080",
        "REMOTE_NAME": "srv"
    },
    "gi2": {
        "LOCAL_IP": "10.0.0.12",
        "LOCAL_PORT": "8182",  
        "LOCAL_NAME": "gi2",
        "REMOTE_IP": "10.0.0.1",
        "REMOTE_PORT": "8080",
        "REMOTE_NAME": "srv"
    },
    "gf1": {
        "LOCAL_IP": "10.0.0.3",
        "LOCAL_PORT": "8281",
        "LOCAL_NAME": "gf1",
        "REMOTE_IP": "10.0.0.2",  
        "REMOTE_PORT": "8181",
        "REMOTE_NAME": "gwi"
    },
    "gf2": {
        "LOCAL_IP": "10.0.0.5",
        "LOCAL_PORT": "8282",
        "LOCAL_NAME": "gf2",
        "REMOTE_IP": "10.0.0.2",
        "REMOTE_PORT": "8181",
        "REMOTE_NAME": "gwi"
    },
    "gf3": {
        "LOCAL_IP": "10.0.0.7",
        "LOCAL_PORT": "8283",
        "LOCAL_NAME": "gf3",
        "REMOTE_IP": "10.0.0.2",
        "REMOTE_PORT": "8181",
        "REMOTE_NAME": "gwi"
    },
    "dev1": {
        "LOCAL_IP": "10.0.0.4",
        "LOCAL_PORT": "9001",
        "LOCAL_NAME": "dev1",
        "REMOTE_IP": "10.0.0.3",
        "REMOTE_PORT": "8281",
        "REMOTE_NAME": "gf1",
        "SEND_PERIOD": "1000"
    },
    "dev2": {
        "LOCAL_IP": "10.0.0.6",
        "LOCAL_PORT": "9002",
        "LOCAL_NAME": "dev2",
        "REMOTE_IP": "10.0.0.5",
        "REMOTE_PORT": "8282",
        "REMOTE_NAME": "gf2",
        "SEND_PERIOD": "3000"
    },
    "dev3": {
        "LOCAL_IP": "10.0.0.8",
        "LOCAL_PORT": "9003",
        "LOCAL_NAME": "dev3",
        "REMOTE_IP": "10.0.0.7",
        "REMOTE_PORT": "8283",
        "REMOTE_NAME": "gf3",
        "SEND_PERIOD": "3000"
    },
    "app": {
        "REMOTE_IP": "127.0.0.1", 
        "REMOTE_PORT": "8080",
        "DEVICE_NAME": "dev1",
        "SEND_PERIOD": "5000"
    }
}
