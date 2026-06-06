import requests
import json
from datetime import datetime

def send_to_elk(log_data):
    """Sends a log entry to Elasticsearch."""
    es_url = "http://localhost:9200/iot-ids-logs/_doc"
    try:
        # Add timestamp for Kibana
        log_data['@timestamp'] = datetime.utcnow().isoformat()
        response = requests.post(es_url, json=log_data)
        return response.status_code
    except Exception as e:
        print(f"Failed to send to ELK: {e}")
        return None

if __name__ == "__main__":
    # Test sending a dummy log
    sample_log = {
        "event_type": "manual_check",
        "message": "System check from Integration Agent",
        "status": "active"
    }
    print(f"Sending test log to ELK... Status: {send_to_elk(sample_log)}")
