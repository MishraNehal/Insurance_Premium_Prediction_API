# Insurance Premium Prediction API

Predict insurance premium categories from user demographics and lifestyle inputs. Built with FastAPI + scikit-learn, and a Streamlit UI for quick interaction.

— FastAPI • scikit-learn • Pydantic • Streamlit —
commond i will ru
## Overview
This service exposes a REST endpoint that accepts user inputs (age, BMI components, income, city, occupation, smoker status), transforms them into model features, and returns a predicted premium category with confidence and per-class probabilities.

## Features
- Typed request/response validation (Pydantic v2)
- Model loaded once and reused (scikit-learn Pipeline)
- `/predict`, `/model-info`, `/health` endpoints
- Streamlit UI in `Frontend/UI.py`
- CORS and TrustedHost middleware enabled
- Simple smoke tests via `test_api.py`

## Tech Stack
- Backend: FastAPI, Starlette
- ML: scikit-learn
- Data: pandas, numpy
- UI: Streamlit

## Architecture
- `app.py` — FastAPI app (routes, middleware, logging)
- `model/predict.py` — Model load + predict functions
- `schema/` — Pydantic schemas for input/output
- `Frontend/UI.py` — Streamlit client for `/predict`

## Quickstart
Prereqs: Python 3.12, pip

```powershell
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run API
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# (Optional) Run UI
streamlit run Frontend\UI.py

# Smoke-test
python test_api.py
```

## API Reference
### POST `/predict`
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

### GET `/model-info`
Returns model version, type, classes, and feature names.

### GET `/health`
Service and model status.

## Examples (cURL)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "weight": 70.5,
    "height": 1.75,
    "income_lpa": 12.5,
    "smoker": false,
    "city": "Mumbai",
    "occupation": "private_job"
  }'

curl http://localhost:8000/model-info
curl http://localhost:8000/health
```

## Streamlit UI
By default, the UI targets `http://localhost:8000/predict`.
```powershell
streamlit run Frontend\UI.py
```
If your API runs elsewhere:
```powershell
$env:FRONTEND_API_URL="http://<host>:<port>/predict"
streamlit run Frontend\UI.py
```

## Configuration
- `FRONTEND_API_URL` (optional): override the API URL used by the UI.
- Ensure `model/model.pkl` exists. The model is a scikit-learn Pipeline.

## Project Structure
```
.
├─ app.py
├─ model/
│  ├─ model.pkl
│  └─ predict.py
├─ schema/
│  ├─ prediction_response.py
│  └─ user_input.py
├─ Frontend/
│  └─ UI.py
├─ requirements.txt
├─ test_api.py
└─ README.md
```

## Docker
```powershell
# Build
docker build -t insurance-api .
# Run
docker run -p 8000:8000 insurance-api
```

## Troubleshooting
- Connection errors from UI: confirm API is running and reachable at the URL configured.
- `ModuleNotFoundError: sklearn`: activate venv and `pip install -r requirements.txt`.
- 422 validation errors: ensure required fields are provided and valid.

## License
MIT
