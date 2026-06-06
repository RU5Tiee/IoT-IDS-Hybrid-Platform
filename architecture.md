# Hybrid IoT IDS System Architecture

## Overview
A distributed Intrusion Detection System (IDS) combining signature-based detection (Suricata) and ML-based anomaly detection.

## Components
1. **Virtual Edge Node (Docker)**: Runs Suricata to capture and analyze network traffic.
2. **Suricata**: Performs signature-based detection and logs alerts/network data.
3. **ML Anomaly Detection**: Python-based service using Isolation Forest to detect unknown patterns.
4. **ELK Stack**:
   - **Elasticsearch**: Centralized log storage.
   - **Logstash/Filebeat**: Data ingestion and parsing.
   - **Kibana**: Visualization and dashboarding.
5. **FastAPI Integration**: Connects the edge node to the ML model for real-time predictions.

## Data Flow
1. **Traffic Capture**: Network traffic flows through the Edge Node.
2. **Signature Detection**: Suricata analyzes traffic against known signatures; generates `eve.json`.
3. **Feature Extraction**: `feature_extractor.py` parses `eve.json` to extract relevant ML features.
4. **Anomaly Detection**: Extracted features are sent to the FastAPI service.
5. **Prediction**: ML Model (Isolation Forest) predicts "normal" or "anomaly".
6. **Logging**: All alerts (Suricata + ML) are forwarded to the ELK stack.
7. **Visualization**: Kibana displays real-time security posture and threat maps.
