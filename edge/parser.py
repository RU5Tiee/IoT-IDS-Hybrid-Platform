import json
import os
import time
import requests
from feature_extractor import FeatureExtractor

# Configuration
# Path to the eve.json file inside the infrastructure folder
EVE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                        "infrastructure", "suricata", "log", "eve.json")
API_URL = "http://localhost:8000/predict"

class EveParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def follow(self):
        """Generates lines from the file as it's written to, handling rotation."""
        print(f"Watching file: {self.file_path}")
        while True:
            if not os.path.exists(self.file_path):
                print(f"Waiting for {self.file_path} to be created...")
                time.sleep(2)
                continue
            
            with open(self.file_path, 'r') as f:
                # Start at the end of the file to only process NEW events
                f.seek(0, os.SEEK_END)
                last_ino = os.fstat(f.fileno()).st_ino
                
                while True:
                    line = f.readline()
                    if not line:
                        # Check if file was rotated or replaced
                        try:
                            if not os.path.exists(self.file_path) or os.stat(self.file_path).st_ino != last_ino:
                                print("Log rotation detected, reopening file...")
                                break 
                        except FileNotFoundError:
                            break
                        
                        time.sleep(0.5)
                        continue
                    yield line

    def parse_line(self, line):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            return None

def main():
    parser = EveParser(EVE_PATH)
    extractor = FeatureExtractor()
    
    print("--- Edge Parser Service Started ---")
    print(f"Target API: {API_URL}")
    
    for line in parser.follow():
        event_data = parser.parse_line(line)
        if not event_data or event_data.get('event_type') == 'stats':
            continue
            
        # 1. Extract features from the raw Suricata event
        features = extractor.extract_features(event_data)
        
        # Add IP metadata for visualization
        src_ip = event_data.get('src_ip')
        dest_ip = event_data.get('dest_ip')
        
        if not src_ip or not dest_ip:
            continue # Skip events without IP info (like system logs)

        features['src_ip'] = src_ip
        features['dest_ip'] = dest_ip
        
        # 2. Send to ML API for prediction
        try:
            response = requests.post(API_URL, json=features, timeout=1)
            if response.status_code == 200:
                result = response.json()
                if result.get('is_anomaly'):
                    print(f"[!] ANOMALY DETECTED: {features['src_ip']} -> {features['dest_ip']} (Score: {result['anomaly_score']:.4f})")
                else:
                    # Optional: Print normal flows too
                    # print(f"Normal Flow: {features['src_ip']} -> {features['dest_ip']}")
                    pass
        except Exception as e:
            print(f"Error connecting to API: {e}")

if __name__ == "__main__":
    main()
