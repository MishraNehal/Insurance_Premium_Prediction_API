import pickle
import pandas as pd
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MLFlow
MODEL_VERSION = '1.0.0'

# Initialize model as None
model = None
class_labels = []

def load_model():
    """Load the ML model with proper error handling"""
    global model, class_labels
    
    try:
        # Get the correct path for model file
        current_dir = Path(__file__).parent
        model_path = current_dir / 'model.pkl'
        
        logger.info(f"Loading model from: {model_path}")
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        # Get class labels from model
        class_labels = model.classes_.tolist()
        logger.info(f"Model loaded successfully. Classes: {class_labels}")
        
    except FileNotFoundError:
        logger.error(f"Model file not found at {model_path}")
        raise Exception("Model file not found. Please ensure model.pkl exists in the model directory.")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise Exception(f"Failed to load model: {str(e)}")

def predict_output(user_input: dict):
    """Predict insurance premium category with error handling"""
    
    try:
        # Ensure model is loaded
        if model is None:
            load_model()
        
        # Validate input
        required_features = ['bmi', 'age_group', 'lifestyle_risk', 'city_tier', 'income_lpa', 'occupation']
        missing_features = [feature for feature in required_features if feature not in user_input]
        
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        # Create DataFrame
        df = pd.DataFrame([user_input])
        logger.info(f"Making prediction for input: {user_input}")
        
        # Predict the class
        predicted_class = model.predict(df)[0]
        
        # Get probabilities for all classes
        probabilities = model.predict_proba(df)[0]
        confidence = max(probabilities)
        
        # Create mapping: {class_name: probability}
        class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))
        
        result = {
            "predicted_category": predicted_class,
            "confidence": round(confidence, 4),
            "class_probabilities": class_probs
        }
        
        logger.info(f"Prediction successful: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise Exception(f"Prediction error: {str(e)}")

# Load model on module import
try:
    load_model()
except Exception as e:
    logger.warning(f"Model will be loaded on first prediction: {str(e)}")