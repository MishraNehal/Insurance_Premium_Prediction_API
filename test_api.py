import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_model_info():
    """Test the model info endpoint"""
    print("Testing model info...")
    response = requests.get(f"{BASE_URL}/model-info")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_prediction():
    """Test the prediction endpoint"""
    print("Testing prediction...")
    
    # Sample input data
    sample_data = {
        "age": 35,
        "weight": 70.5,
        "height": 1.75,
        "income_lpa": 12.5,
        "smoker": False,
        "city": "Mumbai",
        "occupation": "private_job"
    }
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=sample_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Predicted Category: {result['predicted_category']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Class Probabilities: {result['class_probabilities']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_invalid_input():
    """Test with invalid input"""
    print("Testing invalid input...")
    
    # Invalid data (missing required fields)
    invalid_data = {
        "age": 35,
        "weight": 70.5
        # Missing other required fields
    }
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=invalid_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print()

if __name__ == "__main__":
    print("=== Insurance Premium Prediction API Tests ===\n")
    
    try:
        test_health_check()
        test_model_info()
        test_prediction()
        test_invalid_input()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error during testing: {str(e)}")

