import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

class Preprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_cols = [
            'src_port', 'dest_port', 'proto_encoded', 
            'pkts_toserver', 'pkts_toclient', 
            'bytes_toserver', 'bytes_toclient',
            'is_flow', 'is_http', 'is_dns', 'is_tls', 'is_alert'
        ]

    def fit(self, df):
        # Ensure all columns exist
        for col in self.feature_cols:
            if col not in df.columns:
                df[col] = 0
        self.scaler.fit(df[self.feature_cols])

    def transform(self, df):
        # Create a copy to avoid SettingWithCopyWarning or modifying original
        df_proc = df.copy()
        for col in self.feature_cols:
            if col not in df_proc.columns:
                df_proc[col] = 0
        # Ensure correct column order and exclude extra columns
        return self.scaler.transform(df_proc[self.feature_cols])

    def save(self, path):
        joblib.dump(self.scaler, path)

    def load(self, path):
        self.scaler = joblib.load(path)
