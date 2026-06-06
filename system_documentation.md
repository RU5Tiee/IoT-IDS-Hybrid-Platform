# Hybrid IoT IDS: System Documentation

## 1. Dataset Overview
The model was trained using a **Synthetic IoT Traffic Dataset** generated in `ml/train.py`. 
- **Normal Profile**: Mimics standard IoT behaviors (MQTT on 1883, HTTP on 80/443, DNS on 53). It uses Poisson distributions for packet counts and Normal distributions for byte sizes based on typical IoT telemetry patterns.
- **Contamination**: Set at 1%, meaning the model assumes 1% of the training data might be anomalous, defining the decision boundary at an anomaly score of 0.

## 2. Recreating the Findings
To reproduce the accuracy and simulation results:
1. **Clean Environment**: Ensure Python 3.8+ is installed with `pandas`, `scikit-learn`, `fastapi`, and `requests`.
2. **Train**: Run `python ml/train.py`. This generates `model.pkl` and `scaler.pkl`.
3. **Evaluate**: Run `python ml/evaluate.py` to see the Confusion Matrix and F1-scores.
4. **Test**: Start the API (`python api/api.py`) and run the simulation script (`python tests/test_simulation.py`).

## 3. How to Run the Project

### Phase 1: Infrastructure (Docker)
1. Navigate to `infrastructure/`.
2. Run `docker-compose up -d`.
   - This starts Suricata (signature detection) and the ELK stack (visualization).

### Phase 2: ML Inference Engine (FastAPI)
1. Open a new terminal.
2. Run `python api/api.py`.
   - The API will listen on `http://localhost:8000`.

### Phase 3: Edge Processing (The "Glue")
1. In a production setup, you would run the parser:
   ```bash
   python edge/parser.py
   ```
   - This monitors Suricata's `eve.json` and prepares data for the ML API.

## 4. Demonstration Guide

### Step 1: Show Signature Detection (Suricata)
- Point to `infrastructure/suricata/config/suricata.yaml`.
- Explain how it catches known threats using rules.

### Step 2: Show Anomaly Detection (ML)
1. Run the simulation: `python tests/test_simulation.py`.
2. **Explain the contrast**:
   - **Test 1 (Normal)**: Shows a positive score. The IDS allows it through.
   - **Test 2 (Flood)**: Shows a negative score. The IDS flags it as a "Flood Attack".
   - **Test 3 (Scanner)**: Shows a negative score. The IDS flags "Unusual Port Access" even with low volume.

### Step 3: Show Robustness (The "Secret Sauce")
- Mention the **Log Rotation Handling**: Explain that if Suricata restarts or logs rotate, the system won't crash (implemented in `edge/parser.py`).
- Show the **Preprocessing Safety**: Explain how the system handles missing data without crashing.

## 5. Summary of Architecture
- **Signature-based**: Catches known CVEs.
- **Anomaly-based**: Catches Zero-Days and behavioral shifts (e.g., a thermostat suddenly sending 50MB of data).
- **Integration**: FastAPI connects the lightweight edge node to the heavy ML model.
