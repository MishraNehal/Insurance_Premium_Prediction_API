from pydantic import BaseModel, Field
from typing import Dict, Optional, Any

class Metadata(BaseModel):
    model_version: str = Field(..., description="Version of the model used for prediction")
    input_features: Dict[str, Any] = Field(..., description="Processed input features used for prediction")

class PredictionResponse(BaseModel):
    predicted_category: str = Field(
        ...,
        description="The predicted insurance premium category",
        example="High"
    )
    confidence: float = Field(
        ...,
        description="Model's confidence score for the predicted class (range: 0 to 1)",
        example=0.8432,
        ge=0.0,
        le=1.0
    )
    class_probabilities: Dict[str, float] = Field(
        ...,
        description="Probability distribution across all possible classes",
        example={"Low": 0.01, "Medium": 0.15, "High": 0.84}
    )
    metadata: Optional[Metadata] = Field(
        None,
        description="Additional metadata about the prediction"
    )
