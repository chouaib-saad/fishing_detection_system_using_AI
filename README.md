# 🔒 Phishing Website Detection System

A machine learning-powered web application that analyzes URLs to detect potential phishing websites in real-time.

![Status](https://img.shields.io/badge/status-active-success.svg)
![ML Model](https://img.shields.io/badge/ML-Random%20Forest-blue.svg)
![Accuracy](https://img.shields.io/badge/accuracy-96.43%25-brightgreen.svg)

## 🌟 Features

- **Real-time URL Analysis** - Instant phishing detection with confidence scores
- **Machine Learning Model** - Random Forest classifier with 96.43% accuracy
- **Beautiful Dark UI** - Modern, responsive interface with glassmorphism design
- **Feature Extraction** - Analyzes 11 URL characteristics
- **Detailed Results** - Shows confidence scores, detection mode, and extracted features
- **No External Dependencies** - Works completely offline

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install flask scikit-learn pandas numpy joblib tldextract
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5001
   ```

## 📊 How It Works

### Feature Extraction

The system analyzes each URL based on 6 key features:

| Feature | Description | Weight |
|---------|-------------|--------|
| **URL Length** | Total character count | 44.39% |
| **Subdomain Count** | Number of subdomains | 27.94% |
| **Has IP** | Contains IP address | 8.99% |
| **Has Dash** | Contains dash characters | 8.26% |
| **Is HTTPS** | Uses HTTPS protocol | 6.63% |
| **Has @ Symbol** | Contains @ character | 3.78% |

### Machine Learning Model

- **Algorithm**: Random Forest Classifier
- **Trees**: 100 estimators
- **Training Data**: 420 URLs (210 safe, 210 phishing)
- **Validation**: 5-fold cross-validation
- **Accuracy**: 96.43% ± 1.30%

### Detection Process

1. User enters a URL
2. System extracts structural features
3. ML model predicts phishing probability
4. Results displayed with confidence score

## 🧪 Testing

See [TEST_URLS.md](TEST_URLS.md) for a comprehensive list of test URLs.

### Quick Test Examples

**Safe URLs:**
- `https://google.com` → SAFE (99.36%)
- `https://github.com` → SAFE (99.36%)
- `https://microsoft.com` → SAFE (99.36%)

**Phishing URLs:**
- `http://192.168.1.1/paypal-verify.com` → PHISHING (100%)
- `https://secure-account-verify.tk` → PHISHING (91.95%)
- `https://google.com@malicious.com` → PHISHING (95%+)

## 📁 Project Structure

```
phishing-detection-system/
├── app.py                      # Flask web application
├── model/
│   ├── phishing_model.pkl      # Trained ML model
│   └── train_model.py          # Model training script
├── utils/
│   └── feature_extractor.py    # URL feature extraction
├── templates/
│   └── index.html              # Web interface
├── static/
│   ├── style.css               # Styling (dark theme)
│   └── script.js               # Frontend logic
├── sample_phishing_data.csv    # Training dataset
├── TEST_URLS.md                # Test URL examples
└── README.md                   # This file
```

## 🎨 UI Features

- **Dark Theme** - Easy on the eyes with cybersecurity aesthetic
- **Glassmorphism** - Modern frosted glass effect
- **Animated Background** - Subtle gradient animations
- **Responsive Design** - Works on desktop and mobile
- **Loading States** - Smooth transitions and spinners
- **Confidence Bars** - Visual representation of prediction confidence
- **Collapsible Details** - View extracted features on demand

## 🔧 API Endpoints

### `GET /`
Returns the web interface

### `POST /check`
Analyzes a URL for phishing

**Request:**
```
Content-Type: application/x-www-form-urlencoded
Body: url=https://example.com
```

**Response:**
```json
{
  "url": "https://example.com",
  "result": "SAFE",
  "confidence": 0.9936,
  "mode": "ML",
  "features": {
    "url_length": 19,
    "has_ip": 0,
    "has_at_symbol": 0,
    "has_dash": 0,
    "is_https": 1,
    "subdomain_count": 0
  }
}
```

### `GET /api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "mode": "ML"
}
```

## 🔄 Retraining the Model

To retrain the model with updated data:

```bash
python model/train_model.py
```

This will:
1. Load the sample dataset
2. Generate additional synthetic samples
3. Train a new Random Forest model
4. Save the model to `model/phishing_model.pkl`
5. Display accuracy metrics and feature importance

## 🛡️ Security Notes

⚠️ **Important**: This is a demonstration project for educational purposes.

- The model analyzes URL **structure only**, not actual website content
- Real-world phishing detection requires more sophisticated analysis
- Always verify URLs through official channels
- Never enter credentials on suspicious websites
- Use this as one layer in a multi-layered security approach

## 📈 Model Performance

### Cross-Validation Results
- **Mean Accuracy**: 96.43%
- **Standard Deviation**: ±1.30%
- **Training Samples**: 420 URLs
- **Test Method**: 5-fold cross-validation

### Feature Importance
```
url_length          ████████████████████ 44.39%
subdomain_count     ███████████ 27.94%
has_ip              ███ 8.99%
has_dash            ███ 8.26%
is_https            ██ 6.63%
has_at_symbol       █ 3.78%
```

## 🤝 Contributing

This is an educational project. Feel free to:
- Add more training data
- Improve feature extraction
- Enhance the UI/UX
- Add new detection methods

## 📝 License

This project is provided as-is for educational purposes.

## 🎓 Educational Context

Built as part of IBM Cybersecurity Essentials certification coursework to demonstrate:
- Machine learning for security applications
- URL analysis and pattern recognition
- Web application development
- Full-stack integration (Python + Flask + JavaScript)

## 🔗 Links

- **IBM Certificate**: [View Certificate](https://coursera.org/verify/98MLTLTZSE15)
- **GitHub**: [Axulo-Inc](https://github.com/Axulo-Inc)

---

**Made with ❤️ for cybersecurity education**
