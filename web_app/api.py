from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import re
from urllib.parse import urlparse

# 1. Load the Trained Pipeline
# Make sure 'phishing_detection_pipeline.pkl' is in the same folder
try:
    model_pipeline = joblib.load('phishing_detection_pipeline.pkl')
except FileNotFoundError:
    print("Error: Model file not found. Please train and save the model first.")

app = FastAPI()

# 2. CORS Setup (Allow HTML page to talk to this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define Input Data Format
class URLItem(BaseModel):
    url: str

# 4. Feature Extraction Logic (Must exactly match training logic)
def extract_features(url):
    url = str(url)
    # Fix protocol for parsing
    if not url.startswith(('http://', 'https://')):
        url_with_protocol = 'http://' + url
    else:
        url_with_protocol = url
    
    try:
        parsed = urlparse(url_with_protocol)
        hostname = parsed.netloc
        if ':' in hostname: # Remove port if present
            hostname = hostname.split(':')[0]
    except:
        hostname = ""

    features = {
        'url_length': len(url),
        'hostname_length': len(hostname),
        'dot_count': url.count('.'),
        'hyphen_count': url.count('-'),
        'at_count': url.count('@'),
        'question_count': url.count('?'),
        'digit_count': sum(c.isdigit() for c in url),
        'has_ip': 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname) else 0,
        'url_text': url  # We must pass the raw text for the TF-IDF part of the pipeline
    }
    return features

# 5. The Prediction Endpoint
@app.post("/predict")
async def predict_url(item: URLItem):
    try:
        # A. Extract features
        features_dict = extract_features(item.url)
        
        # B. Convert features to DataFrame (Pipeline expects a DataFrame)
        input_df = pd.DataFrame([features_dict])
        
        # C. Get the prediction
        # [0]: Safe, [1]: Malicious
        prediction = model_pipeline.predict(input_df)[0]
        
        # Get probability (Confidence)
        probability = model_pipeline.predict_proba(input_df)[0][1]

        result = "Malicious" if prediction == 1 else "Safe"
        
        return {
            "url": item.url,
            "result": result,
            "confidence_score": float(probability)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))