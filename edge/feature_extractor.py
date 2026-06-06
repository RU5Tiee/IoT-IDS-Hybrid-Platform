import pandas as pd
import numpy as np

class FeatureExtractor:
    def __init__(self):
        self.protocol_map = {'TCP': 6, 'UDP': 17, 'ICMP': 1}
        
    def extract_features(self, event_data):
        """
        Extracts a feature vector from a single Suricata eve.json record.
        Targeting common features for Isolation Forest.
        """
        if not isinstance(event_data, dict):
            return {}

        features = {}
        
        # Core Network Features
        features['src_port'] = event_data.get('src_port', 0)
        features['dest_port'] = event_data.get('dest_port', 0)
        
        # Protocol Encoding
        proto = event_data.get('proto', 'OTHER')
        features['proto_encoded'] = self.protocol_map.get(proto, 0)
        
        # Flow Stats (safely handle nested dict)
        flow = event_data.get('flow', {})
        if not isinstance(flow, dict):
            flow = {}
            
        features['pkts_toserver'] = flow.get('pkts_toserver', 0)
        features['pkts_toclient'] = flow.get('pkts_toclient', 0)
        features['bytes_toserver'] = flow.get('bytes_toserver', 0)
        features['bytes_toclient'] = flow.get('bytes_toclient', 0)
        
        # Event Type Encoding (Simplified)
        event_types = ['flow', 'http', 'dns', 'tls', 'alert']
        current_type = event_data.get('event_type', 'other')
        for et in event_types:
            features[f'is_{et}'] = 1 if current_type == et else 0
            
        return features

    def to_dataframe(self, features_list):
        return pd.DataFrame(features_list).fillna(0)

if __name__ == "__main__":
    extractor = FeatureExtractor()
    sample_event = {
        "event_type": "flow",
        "proto": "TCP",
        "src_port": 44321,
        "dest_port": 80,
        "flow": {"pkts_toserver": 10, "pkts_toclient": 8, "bytes_toserver": 1500, "bytes_toclient": 1200}
    }
    print(extractor.extract_features(sample_event))
