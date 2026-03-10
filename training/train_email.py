import pandas as pd
import joblib
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp.preprocessor import preprocess
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

def train_email_model():
    print("Loading Email dataset...")
    # Load dataset
    df = pd.read_csv('datasets/enron_txt_fn.csv')
    
    # Dataset columns: label, filename
    # Assuming 'filename' contains the email content or the label mapping is needed
    # Let's verify labels
    # 0 -> spam/phishing, 1 -> safe
    # Native Enron dataset: 0 -> ham (safe), 1 -> spam
    # Expected by app.py: 1 -> safe, 0 -> spam/phishing
    if df['label'].dtype == object:
        df['label'] = df['label'].map({'spam': 0, 'ham': 1})
    else:
        # Invert integer labels
        df['label'] = df['label'].map({0: 1, 1: 0})
    
    print("Preprocessing text...")
    df['cleaned_msg'] = df['email'].astype(str).apply(preprocess)
    
    # Feature Extraction
    print("Vectorizing text...")
    tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
    X = tfidf.fit_transform(df['cleaned_msg'])
    y = df['label']
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model Training
    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluation
    y_pred = model.predict(X_test)
    print("\nEmail Model Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))
    
    # Save Model and Vectorizer
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    models_dir = os.path.join(BASE_DIR, 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        
    save_path_model = os.path.join(models_dir, 'email_model.pkl')
    save_path_tfidf = os.path.join(models_dir, 'email_vectorizer.pkl')
    
    print(f"Saving models to: {models_dir}")
    joblib.dump(model, save_path_model)
    joblib.dump(tfidf, save_path_tfidf)
    print(f"Saved: {save_path_model}")
    print("Email training complete.")

if __name__ == "__main__":
    train_email_model()
