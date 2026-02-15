import sys
import io
import os
import pandas as pd
import numpy as np
import joblib
import sklearn
from flask import Flask, render_template, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from utils.feature_extractor import extract_features

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "phishing_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "sample_phishing_data.csv")

# Global model variable
model = None

def train_fallback_model():
    """Trains a model on the fly if loading fails (Vercel compatibility fix)"""
    print("🔄 Starting fallback training...")
    try:
        # Load data
        if not os.path.exists(DATA_PATH):
            print("❌ Training data not found!")
            return None
            
        df = pd.read_csv(DATA_PATH)
        
        # Features needed
        feature_cols = ["url_length", "has_ip", "has_at_symbol", "has_dash", "is_https", "subdomain_count"]
        
        # Train basic model
        X = df[feature_cols]
        y = df["label"]
        
        clf = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
        clf.fit(X, y)
        
        print("✅ Fallback model trained successfully!")
        return clf
    except Exception as e:
        print(f"❌ Fallback training failed: {e}")
        return None

# Try to load model, otherwise train
try:
    print(f"📂 Loading model from: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded from file!")
except Exception as e:
    print(f"⚠️ Load failed ({e}). Attempting fallback training...")
    model = train_fallback_model()

# Final check
if model:
    print("🚀 System Online: ML Mode")
else:
    print("⚠️ System Online: Heuristic Mode (Limited)")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_url():
    url = request.form.get("url", "")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Extract features
        features_dict = extract_features(url)
        
        # Prepare for prediction
        feature_cols = ["url_length", "has_ip", "has_at_symbol", "has_dash", "is_https", "subdomain_count"]
        features_df = pd.DataFrame([features_dict])
        
        # Ensure columns exist
        for col in feature_cols:
            if col not in features_df.columns:
                features_df[col] = 0
        
        # Reorder
        X_pred = features_df[feature_cols]

        if model:
            # ML Prediction
            prob = model.predict_proba(X_pred)[0][1] # Probability of phishing
            prediction = "PHISHING" if prob > 0.5 else "SAFE"
            mode = "ML"
            
            # Confidence logic
            confidence = prob if prediction == "PHISHING" else (1 - prob)
            
        else:
            # Heuristic Fallback
            mode = "Heuristic"
            score = 0
            if features_dict.get('has_ip', 0): score += 30
            if features_dict.get('url_length', 0) > 75: score += 20
            if features_dict.get('has_at_symbol', 0): score += 20
            
            if score > 40:
                prediction = "PHISHING"
                confidence = 0.8
            else:
                prediction = "SAFE"
                confidence = 0.7

        return jsonify({
            "url": url,
            "result": prediction,
            "confidence": float(confidence),
            "mode": mode,
            "features": features_dict
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "result": "ERROR", "confidence": 0}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
