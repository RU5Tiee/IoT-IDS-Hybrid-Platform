import requests
import json
import time

API_URL = "http://localhost:8000/predict"

def test_case(name, features):
    print(f"--- Running Test: {name} ---")
    try:
        response = requests.post(API_URL, json=features)
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction: {result['prediction']}")
            print(f"Is Anomaly: {result['is_anomaly']}")
            print(f"Score: {result['anomaly_score']:.4f}")
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Connection Failed: Ensure api.py is running. {e}")
    print("\n")

if __name__ == "__main__":
    # Test 1: Normal MQTT Traffic
    normal_traffic = {
        "src_ip": "192.168.1.50",
        "dest_ip": "10.0.0.5",
        "src_port": 45123,
        "dest_port": 1883,
        "proto_encoded": 6,
        "pkts_toserver": 12,
        "pkts_toclient": 10,
        "bytes_toserver": 1200,
        "bytes_toclient": 800,
        "is_flow": 1
    }
    
    # Test 2: Potential Flood Attack (Anomaly)
    flood_traffic = {
        "src_ip": "172.16.0.100",
        "dest_ip": "192.168.1.1",
        "src_port": 6666,
        "dest_port": 80,
        "proto_encoded": 6,
        "pkts_toserver": 5000,
        "pkts_toclient": 5,
        "bytes_toserver": 250000,
        "bytes_toclient": 400,
        "is_flow": 1,
        "is_alert": 1
    }

    # Test 3: Unusual Port Access (Anomaly)
    scan_traffic = {
        "src_ip": "10.0.0.200",
        "dest_ip": "192.168.1.50",
        "src_port": 1234,
        "dest_port": 22,
        "proto_encoded": 6,
        "pkts_toserver": 1,
        "pkts_toclient": 0,
        "bytes_toserver": 60,
        "bytes_toclient": 0,
        "is_flow": 1
    }

    print("Note: Ensure API is running at http://localhost:8000\n")
    test_case("Normal Traffic", normal_traffic)
    test_case("Flood Attack", flood_traffic)
    test_case("Unusual Port Access", scan_traffic)
