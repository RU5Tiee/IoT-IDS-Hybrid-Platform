from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import sys
import os
import requests
from datetime import datetime
from typing import Optional

# Define project root and add ml to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'ml'))
from preprocessing import Preprocessor

app = FastAPI(title="Hybrid IoT IDS ML API")

# ELK Configuration
ELASTICSEARCH_URL = "http://localhost:9200/iot-ids-logs/_doc"

def send_to_elk(data):
    """Utility to send prediction results to Elasticsearch."""
    try:
        # Add timestamp for Kibana
        data['@timestamp'] = datetime.utcnow().isoformat()
        requests.post(ELASTICSEARCH_URL, json=data, timeout=1)
    except Exception as e:
        print(f"ELK Logging Error: {e}")

# Path to artifacts
MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'ml', 'scaler.pkl')

# Global variables for model and preprocessor
model = None
preprocessor = None

class FeatureVector(BaseModel):
    # Metadata for visualization (not used in ML prediction)
    src_ip: Optional[str] = "unknown"
    dest_ip: Optional[str] = "unknown"
    
    # Features for ML Prediction
    src_port: int
    dest_port: int
    proto_encoded: int
    pkts_toserver: int
    pkts_toclient: int
    bytes_toserver: float
    bytes_toclient: float
    is_flow: int = 0
    is_http: int = 0
    is_dns: int = 0
    is_tls: int = 0
    is_alert: int = 0

@app.on_event("startup")
def load_artifacts():
    global model, preprocessor
    try:
        model = joblib.load(MODEL_PATH)
        preprocessor = Preprocessor()
        preprocessor.load(SCALER_PATH)
        print(f"Model and Scaler loaded successfully from {BASE_DIR}.")
    except Exception as e:
        print(f"Error loading model artifacts: {e}")

@app.get("/")
def read_root():
    return {"message": "IoT IDS ML API is running"}

@app.post("/predict")
def predict(features: FeatureVector):
    if model is None or preprocessor is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert Pydantic model to DataFrame
        feature_dict = features.model_dump()
        
        # We only pass the numeric features to the preprocessor/model
        # Preprocessor.transform will automatically handle missing/extra cols based on its feature_cols list
        df = pd.DataFrame([feature_dict])
        
        # Preprocess (only uses the columns defined in Preprocessor.feature_cols)
        X = preprocessor.transform(df)
        
        # Predict
        prediction = model.predict(X)[0] # 1 for normal, -1 for anomaly
        score = model.decision_function(X)[0] # Lower is more anomalous
        
        # Construct the final result including the IPs for logging
        result = {
            "src_ip": features.src_ip,
            "dest_ip": features.dest_ip,
            "prediction": "normal" if prediction == 1 else "anomaly",
            "is_anomaly": bool(prediction == -1),
            "anomaly_score": float(score),
            "features": feature_dict
        }

        # Send to ELK for Kibana visualization
        send_to_elk(result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
