import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import sys
import os

# Ensure we can import from the current directory for Preprocessor
sys.path.append(os.path.abspath('ml'))
from preprocessing import Preprocessor

def generate_test_data(n_normal=1000, n_anomaly=200):
    """Generates a labeled test dataset."""
    np.random.seed(44)
    
    # Normal data
    normal_data = {
        'src_port': np.random.randint(1024, 65535, n_normal),
        'dest_port': np.random.choice([80, 443, 53, 1883], n_normal),
        'proto_encoded': np.random.choice([6, 17], n_normal),
        'pkts_toserver': np.random.poisson(10, n_normal),
        'pkts_toclient': np.random.poisson(12, n_normal),
        'bytes_toserver': np.random.normal(1000, 200, n_normal),
        'bytes_toclient': np.random.normal(1500, 300, n_normal),
        'is_flow': np.ones(n_normal),
        'is_http': np.random.binomial(1, 0.3, n_normal),
        'is_dns': np.random.binomial(1, 0.2, n_normal),
        'is_tls': np.random.binomial(1, 0.1, n_normal),
        'is_alert': np.zeros(n_normal)
    }
    df_normal = pd.DataFrame(normal_data)
    df_normal['label'] = 1  # 1 for Normal in IsolationForest prediction terms (usually 1 is inlier)

    # Anomaly data (e.g., port scanning or high volume)
    anomaly_data = {
        'src_port': np.random.randint(1024, 65535, n_anomaly),
        'dest_port': np.random.randint(1, 1024, n_anomaly), # Abnormal ports
        'proto_encoded': np.random.choice([6, 17], n_anomaly),
        'pkts_toserver': np.random.poisson(500, n_anomaly), # Flood attack
        'pkts_toclient': np.random.poisson(10, n_anomaly),
        'bytes_toserver': np.random.normal(50000, 5000, n_anomaly),
        'bytes_toclient': np.random.normal(500, 100, n_anomaly),
        'is_flow': np.ones(n_anomaly),
        'is_http': np.zeros(n_anomaly),
        'is_dns': np.zeros(n_anomaly),
        'is_tls': np.zeros(n_anomaly),
        'is_alert': np.ones(n_anomaly) # High alerts
    }
    df_anomaly = pd.DataFrame(anomaly_data)
    df_anomaly['label'] = -1 # -1 for Outlier in IsolationForest prediction terms

    df_test = pd.concat([df_normal, df_anomaly]).sample(frac=1).reset_index(drop=True)
    return df_test

def evaluate():
    print("Loading model and data...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model = joblib.load(os.path.join(base_dir, 'model.pkl'))
    preprocessor = Preprocessor()
    preprocessor.load(os.path.join(base_dir, 'scaler.pkl'))
    
    df_test = generate_test_data()
    y_true = df_test['label']
    X_test = preprocessor.transform(df_test.drop(columns=['label']))
    
    print("Running evaluation...")
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    acc = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    report = classification_report(y_true, y_pred, target_names=['Anomaly (-1)', 'Normal (1)'])
    
    print("\n--- Evaluation Results ---")
    print(f"Accuracy: {acc:.4f}")
    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(report)

if __name__ == "__main__":
    evaluate()
