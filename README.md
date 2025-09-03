# Insurance Premium Prediction API

FastAPI service that predicts insurance premium category using a trained scikit-learn model, plus a Streamlit UI.

## Prerequisites
- Python 3.12 (recommended)
- pip

## Setup

```powershell
# From the project root
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run the API
```powershell
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Test the API
```powershell
python test_api.py
```

## Run the Streamlit Frontend
By default, the UI points to `http://localhost:8000/predict`.
```powershell
streamlit run Frontend\UI.py
```
If your API runs elsewhere, set the URL:
```powershell
$env:FRONTEND_API_URL="http://<host>:<port>/predict"
streamlit run Frontend\UI.py
```

## Project Structure
- app.py: FastAPI app (endpoints: /, /health, /predict, /model-info)
- model/: `predict.py`, `model.pkl`
- schema/: Pydantic models
- Frontend/UI.py: Streamlit app

## Docker (optional)
```powershell
# Build
docker build -t insurance-api .
# Run
docker run -p 8000:8000 insurance-api
```

## Notes
- Ensure `model/model.pkl` exists.
- `requirements.txt` includes scikit-learn and streamlit.
