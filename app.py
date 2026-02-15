import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
Phishing Detection System - Professional Edition
Version 2.0.0
"""
from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import os
import sklearn
from utils.feature_extractor import extract_features

# Debug: Print versions
print(f"sklearn version: {sklearn.__version__}")
print(f"pandas version: {pd.__version__}")

app = Flask(__name__)

# Build absolute path to the model file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "phishing_model.pkl")

# Load model
model = None
try:
    print(f"[INFO] Looking for model at: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    print("✅ Machine Learning Model loaded successfully!")
    print("   Running in ML mode")
except Exception as e:
    model = None
    print(f"⚠️ Model not found - running in heuristic mode!")
    print(f"   Error: {e}")
    # Debug: List context to help on Vercel
    try:
        print(f"   Current Directory: {os.getcwd()}")
        print(f"   Base Directory: {BASE_DIR}")
        print(f"   Listing Base Directory:")
        for f in os.listdir(BASE_DIR):
            print(f"    - {f}")
        if os.path.exists(os.path.join(BASE_DIR, "model")):
             print(f"   Listing Model Directory:")
             for f in os.listdir(os.path.join(BASE_DIR, "model")):
                 print(f"    - {f}")
    except Exception as d_e:
        print(f"   Debug Error: {d_e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_url():
    url = request.form.get("url", "").strip()
    
    if not url:
        return jsonify({"error": "No URL provided"})
    
    # Extract features
    features_dict = extract_features(url)
    
    # Convert to DataFrame for model prediction
    features_df = pd.DataFrame([features_dict])
    
    # Ensure we have the right features in the right order
    required_features = ["url_length", "has_ip", "has_at_symbol", 
                         "has_dash", "is_https", "subdomain_count"]
    
    # Add missing features with default values
    for feature in required_features:
        if feature not in features_df.columns:
            features_df[feature] = 0
    
    # Reorder columns
    features_df = features_df[required_features]
    
    # Make prediction
    if model is not None:
        try:
            prediction = model.predict(features_df)[0]
            result = "PHISHING DETECTED" if prediction == 1 else "SAFE"
            
            # Get confidence score
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(features_df)[0]
                confidence = proba[1] if prediction == 1 else proba[0]
            else:
                confidence = 0.85 if prediction == 1 else 0.15
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"[ERROR] Prediction failed: {e}")
            print(error_details)
            # Log to file for debugging
            with open("error_log.txt", "a", encoding="utf-8") as f:
                f.write(f"\n=== Error at {pd.Timestamp.now()} ===\n")
                f.write(error_details)
            result = "ERROR in ML prediction"
            confidence = 0.5
    else:
        # Heuristic mode
        if features_dict.get("has_ip", False) or features_dict.get("has_at_symbol", False):
            result = "SUSPICIOUS (Heuristic)"
            confidence = 0.7
        elif features_dict.get("has_dash", False) and features_dict.get("subdomain_count", 0) > 2:
            result = "SUSPICIOUS (Heuristic)"
            confidence = 0.6
        else:
            result = "LIKELY SAFE (Heuristic)"
            confidence = 0.3
    
    return jsonify({
        "url": url,
        "result": result,
        "confidence": float(confidence),
        "features": features_dict,
        "mode": "ML" if model is not None else "Heuristic"
    })

@app.route("/api/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "mode": "ML" if model is not None else "Heuristic"
    })

if __name__ == "__main__":
    print("[INFO] Starting Phishing Detection System on http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
