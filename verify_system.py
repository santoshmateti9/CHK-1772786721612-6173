import requests
import json

BASE_URL = "http://localhost:5000"

def test_prediction(endpoint, data, expected_prediction):
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, json=data)
    result = response.json()
    prediction = result.get("prediction")
    status = "PASS" if prediction == expected_prediction else "FAIL"
    print(f"Testing {endpoint}: {data}")
    print(f"Result: {prediction} (Expected: {expected_prediction}) -> {status}\n")

print("--- AI Phishing and Spam Detection Verification ---\n")

# SMS Verification
test_prediction("/predict/sms", {"message": "You won a free lottery! Click here to claim prize"}, "spam")
test_prediction("/predict/sms", {"message": "Are we meeting tomorrow?"}, "safe")

# Email Verification
test_prediction("/predict/email", {"message": "Verify your bank account immediately by clicking this link"}, "spam")
test_prediction("/predict/email", {"message": "Please find attached the meeting agenda"}, "safe")

# URL Verification
test_prediction("/predict/url", {"url": "http://secure-login-bank-update.xyz"}, "spam")
test_prediction("/predict/url", {"url": "https://www.google.com"}, "safe")
