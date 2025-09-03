from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
import time
from typing import Dict, Any
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Insurance Premium Prediction API",
    description="A FastAPI application that predicts insurance premium categories based on user demographics and health factors",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and their processing time"""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response time
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
    
    return response

@app.get('/', tags=["General"])
async def home():
    """
    Home endpoint providing basic API information
    """
    return {
        'message': 'Insurance Premium Prediction API',
        'version': '1.0.0',
        'docs': '/docs',
        'health': '/health'
    }

@app.get('/health', tags=["Monitoring"])
async def health_check():
    """
    Health check endpoint to verify API and model status
    """
    try:
        model_status = model is not None
        return {
            'status': 'healthy' if model_status else 'unhealthy',
            'version': MODEL_VERSION,
            'model_loaded': model_status,
            'timestamp': time.time()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.post('/predict', response_model=PredictionResponse, tags=["Prediction"])
async def predict_premium(data: UserInput):
    """
    Predict insurance premium category based on user input
    
    **Input Parameters:**
    - **age**: User's age (1-119)
    - **weight**: User's weight in kg
    - **height**: User's height in meters
    - **income_lpa**: Annual salary in LPA
    - **smoker**: Whether user is a smoker
    - **city**: User's city
    - **occupation**: User's occupation
    
    **Returns:**
    - **predicted_category**: Predicted premium category
    - **confidence**: Model confidence score
    - **class_probabilities**: Probability distribution across all classes
    """
    
    try:
        # Prepare user input for model
        user_input = {
            'bmi': data.bmi,
            'age_group': data.age_group,
            'lifestyle_risk': data.lifestyle_risk,
            'city_tier': data.city_tier,
            'income_lpa': data.income_lpa,
            'occupation': data.occupation
        }
        
        logger.info(f"Processing prediction request for user: age={data.age}, city={data.city}")
        
        # Get prediction
        prediction = predict_output(user_input)
        
        # Add metadata to response
        response_data = {
            "predicted_category": prediction["predicted_category"],
            "confidence": prediction["confidence"],
            "class_probabilities": prediction["class_probabilities"],
            "metadata": {
                "model_version": MODEL_VERSION,
                "input_features": {
                    "bmi": round(data.bmi, 2),
                    "age_group": data.age_group,
                    "lifestyle_risk": data.lifestyle_risk,
                    "city_tier": data.city_tier,
                    "income_lpa": data.income_lpa,
                    "occupation": data.occupation
                }
            }
        }
        
        logger.info(f"Prediction successful: {prediction['predicted_category']} with confidence {prediction['confidence']}")
        return response_data
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction")

@app.get('/model-info', tags=["Model"])
async def get_model_info():
    """
    Get information about the loaded model
    """
    try:
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        return {
            "model_version": MODEL_VERSION,
            "model_type": type(model).__name__,
            "classes": model.classes_.tolist() if hasattr(model, 'classes_') else [],
            "features": getattr(model, 'feature_names_in_', []).tolist() if hasattr(model, 'feature_names_in_') else []
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving model information")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )





