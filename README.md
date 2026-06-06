# Hybrid IoT Intrusion Detection System

## Overview
This repository contains a hybrid Intrusion Detection System (IDS) optimized for Internet of Things (IoT) network topologies. The architecture combines deterministic signature-based detection via Suricata with probabilistic machine learning anomaly detection using an Isolation Forest algorithm. All system logs and detection metrics are aggregated and visualized using the ELK Stack (Elasticsearch, Logstash, Kibana).

## Architecture

The system operates across a decoupled edge-to-cloud architecture to ensure high throughput packet capture without resource starvation at the inference layer.

![Architecture: ML Inference](docs/images/phase3.png)

1. **Traffic Capture (Suricata)**: Operates at the network edge, monitoring incoming packets against predefined CVE and threat signatures. Outputs are logged continuously to `eve.json`.
2. **Log Processing**: A resilient edge parser tails `eve.json` to handle missing fields and log rotation. It extracts specific network features (e.g., packet counts, byte volumes, ports) and converts them into normalized numerical vectors.
3. **ML Inference (FastAPI)**: The extracted feature vectors are transmitted to a backend API running an Isolation Forest model. This engine evaluates traffic patterns against learned baseline distributions to detect zero-day anomalies such as SYN floods or abnormal DNS querying.
4. **Data Aggregation**: Alerts and scoring outputs from both engines are shipped to Elasticsearch for indexing and visualized via Kibana dashboards.

## Machine Learning Implementation

The anomaly detection component leverages the **Isolation Forest** algorithm, trained specifically on synthetic IoT traffic profiles mimicking protocols like MQTT, HTTP, and DNS.

### Model Metrics
The model was evaluated against a dataset simulating 1% contamination (anomalous traffic).

- **Algorithm**: Isolation Forest (Scikit-Learn)
- **Accuracy**: 90.50%
- **Precision (Anomaly)**: 0.86
- **Recall (Anomaly)**: 0.51
- **F1-Score (Normal)**: 0.95
- **F1-Score (Anomaly)**: 0.64

**Confusion Matrix**:
```text
[[ 102   98]
 [  16  984]]
```
*Analysis*: The model demonstrates high precision in identifying anomalies (86%). The conservative recall (51%) is an explicit tuning choice to minimize false positives, which is critical in high-volume IoT telemetry environments.

## Directory Structure

- `api/`: FastAPI backend exposing ML inference endpoints.
- `edge/`: Middleware parser and feature extraction scripts handling Suricata logs.
- `infrastructure/`: Docker Compose deployments for Suricata and the ELK stack.
- `ml/`: Model training pipelines, preprocessing configurations, and serialized models (`model.pkl`, `scaler.pkl`).
- `tests/`: End-to-end traffic pattern simulations and validation tests.
- `docs/`: System documentation and architectural diagrams.

## Deployment Guide

1. **Initialize Infrastructure**
   Deploy Suricata and the ELK stack via Docker:
   ```bash
   cd infrastructure
   docker-compose up -d
   ```

2. **Start the Inference API**
   Launch the FastAPI backend to serve the ML model:
   ```bash
   python api/api.py
   ```

3. **Run the Edge Parser**
   Begin parsing logs and transmitting feature vectors to the API:
   ```bash
   python edge/parser.py
   ```
