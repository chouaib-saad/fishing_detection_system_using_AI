"""
Train a Random Forest model for phishing URL detection.
Uses the sample_phishing_data.csv dataset.
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import joblib
import os
import numpy as np

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "sample_phishing_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "phishing_model.pkl")

# Feature columns the model will use
FEATURE_COLS = ["url_length", "has_ip", "has_at_symbol", "has_dash", "is_https", "subdomain_count"]

def generate_extended_dataset():
    """
    Generate an extended training dataset with more samples for better accuracy.
    Combines the original CSV data with synthetically generated realistic samples.
    """
    # Load original data
    df_original = pd.read_csv(DATA_PATH)
    
    print(f"[INFO] Original dataset: {len(df_original)} samples")
    
    # Generate additional synthetic safe URLs
    np.random.seed(42)
    safe_samples = []
    for _ in range(200):
        safe_samples.append({
            "url_length": np.random.randint(12, 40),
            "has_ip": 0,
            "has_at_symbol": 0,
            "has_dash": np.random.choice([0, 1], p=[0.7, 0.3]),
            "is_https": np.random.choice([1, 0], p=[0.85, 0.15]),
            "subdomain_count": np.random.choice([0, 1], p=[0.8, 0.2]),
            "label": 0
        })
    
    # Generate additional synthetic phishing URLs
    phishing_samples = []
    for _ in range(200):
        phishing_samples.append({
            "url_length": np.random.randint(25, 80),
            "has_ip": np.random.choice([1, 0], p=[0.35, 0.65]),
            "has_at_symbol": np.random.choice([1, 0], p=[0.25, 0.75]),
            "has_dash": np.random.choice([1, 0], p=[0.75, 0.25]),
            "is_https": np.random.choice([0, 1], p=[0.55, 0.45]),
            "subdomain_count": np.random.choice([0, 1, 2, 3, 4], p=[0.15, 0.25, 0.25, 0.2, 0.15]),
            "label": 1
        })
    
    df_safe = pd.DataFrame(safe_samples)
    df_phishing = pd.DataFrame(phishing_samples)
    
    # Combine all data
    df_combined = pd.concat([df_original[FEATURE_COLS + ["label"]], df_safe, df_phishing], ignore_index=True)
    
    # Shuffle
    df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"[INFO] Extended dataset: {len(df_combined)} samples")
    print(f"       Safe: {(df_combined['label'] == 0).sum()}, Phishing: {(df_combined['label'] == 1).sum()}")
    
    return df_combined


def train_model():
    """Train and save the Random Forest phishing detection model."""
    
    print("=" * 50)
    print("  Phishing Detection Model Training")
    print("=" * 50)
    
    # Get data
    df = generate_extended_dataset()
    
    X = df[FEATURE_COLS]
    y = df["label"]
    
    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    # Cross-validation
    scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    print(f"\n[RESULTS] Cross-Validation Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")
    
    # Train on full dataset
    model.fit(X, y)
    
    # Feature importance
    print("\n[INFO] Feature Importances:")
    for name, importance in sorted(zip(FEATURE_COLS, model.feature_importances_), key=lambda x: -x[1]):
        bar = "#" * int(importance * 40)
        print(f"       {name:20s} {importance:.4f} {bar}")
    
    # Save model
    joblib.dump(model, MODEL_PATH)
    print(f"\n[OK] Model saved to: {MODEL_PATH}")
    
    # Quick sanity test
    print("\n[TEST] Quick predictions:")
    test_cases = [
        {"url_length": 18, "has_ip": 0, "has_at_symbol": 0, "has_dash": 0, "is_https": 1, "subdomain_count": 0},  # google.com
        {"url_length": 35, "has_ip": 1, "has_at_symbol": 0, "has_dash": 1, "is_https": 0, "subdomain_count": 4},  # phishing
        {"url_length": 20, "has_ip": 0, "has_at_symbol": 0, "has_dash": 0, "is_https": 1, "subdomain_count": 0},  # safe
        {"url_length": 60, "has_ip": 0, "has_at_symbol": 1, "has_dash": 1, "is_https": 0, "subdomain_count": 3},  # phishing
    ]
    labels = ["google.com (safe)", "IP-based phishing", "normal site (safe)", "complex phishing"]
    
    test_df = pd.DataFrame(test_cases)
    predictions = model.predict(test_df)
    probabilities = model.predict_proba(test_df)
    
    for label, pred, proba in zip(labels, predictions, probabilities):
        result = "PHISHING" if pred == 1 else "SAFE"
        conf = proba[1] if pred == 1 else proba[0]
        print(f"       {label:25s} -> {result:10s} (confidence: {conf:.2%})")
    
    print("\n" + "=" * 50)
    print("  Training complete!")
    print("=" * 50)


if __name__ == "__main__":
    train_model()
