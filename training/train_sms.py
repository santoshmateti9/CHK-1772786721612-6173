import pandas as pd
import joblib
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp.preprocessor import preprocess
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score

def train_sms_model():
    # Load dataset using absolute path
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    dataset_path = os.path.join(BASE_DIR, 'datasets', 'spam_ham_india.csv')
    print(f"Loading SMS dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    # Rename columns if necessary (Msg, Label)
    # 0 -> spam/phishing, 1 -> safe
    # Map 'spam' to 0 and 'ham' to 1 if binary labels are strings
    if df['Label'].dtype == object:
        df['Label'] = df['Label'].map({'spam': 0, 'ham': 1})
    
    print("Preprocessing text...")
    df['cleaned_msg'] = df['Msg'].apply(preprocess)
    
    # Feature Extraction
    print("Vectorizing text...")
    tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
    X = tfidf.fit_transform(df['cleaned_msg'])
    y = df['Label']
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model Training
    print("Training Linear SVM model...")
    model = LinearSVC(random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluation
    y_pred = model.predict(X_test)
    print("\nSMS Model Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))
    
    # Save Model and Vectorizer
    models_dir = os.path.join(BASE_DIR, 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    
    save_path_model = os.path.join(models_dir, 'sms_model.pkl')
    save_path_tfidf = os.path.join(models_dir, 'sms_vectorizer.pkl')
    
    print(f"Saving models to: {models_dir}")
    joblib.dump(model, save_path_model)
    joblib.dump(tfidf, save_path_tfidf)
    print(f"Saved: {save_path_model}")
    print("SMS training complete.")

if __name__ == "__main__":
    train_sms_model()
