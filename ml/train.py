import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
from preprocessing import Preprocessor
import os

# Note: Scikit-learn's IsolationForest does not natively support GPU.
# For GPU training, one would typically use RAPIDS cuML.
# Since this environment may not have cuML, we use standard sklearn,
# but note that in a real IoT TA-2 setup, cuML is preferred.

def generate_synthetic_data(n_samples=10000):
    """Generates synthetic 'normal' IoT traffic data for training."""
    np.random.seed(42)
    data = {
        'src_port': np.random.randint(1024, 65535, n_samples),
        'dest_port': np.random.choice([80, 443, 53, 1883], n_samples), # Common IoT ports
        'proto_encoded': np.random.choice([6, 17], n_samples),
        'pkts_toserver': np.random.poisson(10, n_samples),
        'pkts_toclient': np.random.poisson(12, n_samples),
        'bytes_toserver': np.random.normal(1000, 200, n_samples),
        'bytes_toclient': np.random.normal(1500, 300, n_samples),
        'is_flow': np.ones(n_samples),
        'is_http': np.random.binomial(1, 0.3, n_samples),
        'is_dns': np.random.binomial(1, 0.2, n_samples),
        'is_tls': np.random.binomial(1, 0.1, n_samples),
        'is_alert': np.zeros(n_samples)
    }
    return pd.DataFrame(data)

def train_model():
    print("Generating/Loading dataset...")
    df = generate_synthetic_data()
    
    preprocessor = Preprocessor()
    preprocessor.fit(df)
    X_train = preprocessor.transform(df)
    
    print("Training Isolation Forest model...")
    # contamination is the expected proportion of outliers
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42, n_jobs=-1)
    model.fit(X_train)
    
    print("Saving model and preprocessor...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    joblib.dump(model, os.path.join(base_dir, 'model.pkl'))
    preprocessor.save(os.path.join(base_dir, 'scaler.pkl'))
    print("Training complete.")

if __name__ == "__main__":
    train_model()
