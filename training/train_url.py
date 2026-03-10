import pandas as pd
import joblib
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score

def train_url_model():
    print("Loading URL dataset...")
  
    df = pd.read_csv('datasets/phiusiil_phishing_url_dataset.csv')
    
    target_column = 'label'
    
    features = [
        'URLLength', 'DomainLength', 'IsDomainIP', 
        'URLSimilarityIndex', 'CharContinuationRate', 'TLDLegitimateProb'
    ]
    
    X = df[features]
    y = df[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    print("\nURL Model Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))
    
    print("Saving models...")
    if not os.path.exists('models'):
        os.makedirs('models')
    joblib.dump(model, 'models/url_model.pkl')
    joblib.dump(scaler, 'models/url_scaler.pkl')
    print("URL training complete.")

if __name__ == "__main__":
    train_url_model()
