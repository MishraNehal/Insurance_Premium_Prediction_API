# Insurance Premium Prediction API

A production-ready FastAPI service that predicts insurance premium categories using a trained scikit-learn model, with a Streamlit UI for easy interaction.

## Features
- FastAPI backend with endpoints for health, prediction, and model info
- Scikit-learn Pipeline model loaded from `model/model.pkl`
- Pydantic validation and typed request/response models
- Streamlit frontend at `Frontend/UI.py`
- CORS and trusted-host middleware configured
- Simple test script to smoke-test endpoints

## Architecture
- `app.py`: FastAPI app exposing `/`, `/health`, `/predict`, `/model-info`
- `model/predict.py`: Model loading and prediction logic
- `schema/`: Pydantic models for request/response
- `Frontend/UI.py`: Streamlit consumer of `/predict`

## Quickstart

### Prerequisites
- Python 3.12
- pip

### Setup
```powershell
# From the project root
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run the API
```powershell
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Run the Streamlit Frontend
By default, the UI points to `http://localhost:8000/predict`.
```powershell
streamlit run Frontend\UI.py
```
If your API runs elsewhere, set the URL before launching:
```powershell
$env:FRONTEND_API_URL="http://<host>:<port>/predict"
streamlit run Frontend\UI.py
```

### Smoke Test the API
```powershell
python test_api.py
```

## API Reference

### POST /predict
- Predicts an insurance premium category.

Request body (example):
```json
{
  "age": 35,
  "weight": 70.5,
  "height": 1.75,
  "income_lpa": 12.5,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

Response (example):
```json
{
  "predicted_category": "Low",
  "confidence": 0.76,
  "class_probabilities": {"High": 0.01, "Low": 0.76, "Medium": 0.23},
  "metadata": {
    "model_version": "1.0.0",
    "input_features": {
      "bmi": 23.02,
      "age_group": "adult",
      "lifestyle_risk": "low",
      "city_tier": 1,
      "income_lpa": 12.5,
      "occupation": "private_job"
    }
  }
}
```

### GET /model-info
Returns model version, type, classes, and feature names.

### GET /health
Indicates service and model load status.

## Environment Variables
- `FRONTEND_API_URL` (optional): Override the API endpoint used by Streamlit UI. Example: `http://localhost:8000/predict`.

## Docker (optional)
```powershell
# Build
docker build -t insurance-api .
# Run
docker run -p 8000:8000 insurance-api
```

## Troubleshooting
- "Could not connect to the FastAPI server": ensure the API is running and reachable at the URL configured in the UI.
- Missing `sklearn` error: install requirements via `pip install -r requirements.txt` while your venv is active.
- Validate the model file exists at `model/model.pkl`.

## Git & GitHub Workflow

### Initialize (already done here)
```powershell
git init
git add .
git commit -m "Initial commit"
```

### Create GitHub Repo and Push (HTTPS)
1. Create an empty repository on GitHub (no README/license).
2. Add remote and push:
```powershell
git remote add origin https://github.com/<YOUR_USER>/<REPO_NAME>.git
git branch -M main
git push -u origin main
```

### Clone (pull) This Project
```powershell
# Clone once
git clone https://github.com/<YOUR_USER>/<REPO_NAME>.git
cd <REPO_NAME>

# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run API
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Run UI
streamlit run Frontend\UI.py
```

### Pull Latest Changes Later
```powershell
cd <REPO_NAME>
git pull origin main
```

## License
Add a license of your choice (MIT recommended). Create a `LICENSE` file at repo root.
