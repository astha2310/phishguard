from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from features import extract_features

app = Flask(__name__)

# Load model and feature columns
print("Loading model...")
model = joblib.load('models/best_model.pkl')
feature_cols = joblib.load('models/feature_cols.pkl')
print("Model loaded! Random Forest - 99.90% AUC-ROC")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    if not url.startswith('http'):
        url = 'http://' + url

    try:
        features = extract_features(url)
        if not features:
            return jsonify({'error': 'Could not extract features'}), 400

        df = pd.DataFrame([features])[feature_cols]

        prediction = int(model.predict(df)[0])
        proba = model.predict_proba(df)[0]
        confidence = float(proba[prediction])

        return jsonify({
            'url': url,
            'prediction': prediction,
            'confidence': confidence,
            'label': 'PHISHING' if prediction == 1 else 'SAFE',
            'features': features
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def stats():
    return jsonify({
        'model': 'Random Forest',
        'auc_roc': 0.9990,
        'training_samples': 6500,
        'features': len(feature_cols),
        'status': 'running'
    })

if __name__ == '__main__':
    print("Starting PhishGuard...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
