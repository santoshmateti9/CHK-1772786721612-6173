from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp.preprocessor import preprocess
from nlp.url_features import extract_url_features

from flask_cors import CORS

# Configure static folder to serve frontend files
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Load Models using absolute paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
models_dir = os.path.join(BASE_DIR, 'models')

print(f"Loading models from: {models_dir}")

sms_model = joblib.load(os.path.join(models_dir, 'sms_model.pkl'))
sms_vectorizer = joblib.load(os.path.join(models_dir, 'sms_vectorizer.pkl'))

email_model = joblib.load(os.path.join(models_dir, 'email_model.pkl'))
email_vectorizer = joblib.load(os.path.join(models_dir, 'email_vectorizer.pkl'))

url_model = joblib.load(os.path.join(models_dir, 'url_model.pkl'))
url_scaler = joblib.load(os.path.join(models_dir, 'url_scaler.pkl'))

@app.route('/predict/sms', methods=['POST'])
def predict_sms():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    cleaned_text = preprocess(data['message'])
    vectorized_text = sms_vectorizer.transform([cleaned_text])
    prediction = sms_model.predict(vectorized_text)[0]
    
    # 0 -> spam/phishing, 1 -> safe
    return jsonify({
        "prediction": "safe" if prediction == 1 else "spam"
    })

@app.route('/predict/email', methods=['POST'])
def predict_email():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    cleaned_text = preprocess(data['message'])
    vectorized_text = email_vectorizer.transform([cleaned_text])
    prediction = email_model.predict(vectorized_text)[0]
    
    return jsonify({
        "prediction": "safe" if prediction == 1 else "spam"
    })

@app.route('/predict/url', methods=['POST'])
def predict_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400
    
    url = data['url']
    # Use the improved feature extraction
    features_dict = extract_url_features(url)
    
    # Whitelist check for common safe domains
    safe_domains = ['google.com', 'microsoft.com', 'facebook.com', 'amazon.com', 'apple.com', 'github.com']
    if any(domain in url.lower() for domain in safe_domains):
        return jsonify({"prediction": "safe"})

    # Ensure features match training order exactly
    feature_names = [
        'URLLength', 'DomainLength', 'IsDomainIP', 
        'URLSimilarityIndex', 'CharContinuationRate', 'TLDLegitimateProb'
    ]
    
    input_data = pd.DataFrame([features_dict])
    
    scaled_features = url_scaler.transform(input_data[feature_names])
    prediction = url_model.predict(scaled_features)[0]
    
    return jsonify({
        "prediction": "safe" if prediction == 1 else "spam"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
