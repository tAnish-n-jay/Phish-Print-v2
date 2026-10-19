from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from feature_extractor import extract_all_features

with open('../models/best_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('../models/feature_pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)

with open('../models/feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)

DROPPED_COLS = ['domain_age_days', 'domain_registration_length']
feature_names_clean = [f for f in feature_names if f not in DROPPED_COLS]

app = FastAPI(title='PhishPrint V2', description='Phishing URL Detection API')

class URLInput(BaseModel):
    url: str

@app.get('/')
def root():
    return {'message': 'PhishPrint V2 API is running'}

@app.post('/predict')
def predict(input: URLInput):
    url = input.url.strip()

    if not url.startswith('http'):
        raise HTTPException(status_code=400, detail='URL must start with http:// or https://')

    features = extract_all_features(url, label=0)

    feature_vector = []
    for col in feature_names_clean:
        val = features.get(col, 0)
        if val is None or val == -1:
            val = 0
        feature_vector.append(float(val))

    X = np.array([feature_vector])
    X_processed = pipeline.transform(X)

    prediction = int(model.predict(X_processed)[0])
    proba = model.predict_proba(X_processed)[0]

    verdict = 'phishing' if prediction == 1 else 'legitimate'
    confidence_score = round(float(proba[prediction]) * 100, 2)

    selector = pipeline.named_steps["selector"]
    selected_mask = selector.get_support()
    selected_features = [feature_names_clean[i] for i in range(len(feature_names_clean)) if selected_mask[i]]

    top_features = {
        feat: round(float(val), 4)
        for feat, val in zip(selected_features, X_processed[0])
    }
    top_5 = dict(sorted(top_features.items(), key=lambda x: abs(x[1]), reverse=True)[:5])

    return {
        "url": str(url),
        "verdict": str(verdict),
        "confidence": confidence_score,
        "top_features": {str(k): float(v) for k, v in top_5.items()}
    }