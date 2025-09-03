import os
import streamlit as st # type: ignore
import requests


# API base URL (override via env var FRONTEND_API_URL if needed)
API_URL = os.getenv("FRONTEND_API_URL", "http://localhost:8000/predict")


st.set_page_config(page_title="Insurance Premium Category Predictor", page_icon="🛡️", layout="centered")
st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below to get a prediction:")


# Input fields
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=1, max_value=119, value=30)
    height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
    smoker = st.selectbox("Are you a smoker?", options=[False, True], index=0)
with col2:
    weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
    income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
    occupation = st.selectbox(
        "Occupation",
        [
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job",
        ],
    )

city = st.text_input("City", value="Mumbai")


def build_payload() -> dict:
    return {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation,
    }


if st.button("Predict Premium Category", type="primary"):
    payload = build_payload()
    try:
        with st.spinner("Contacting API and generating prediction..."):
            response = requests.post(API_URL, json=payload, timeout=15)

        # FastAPI returns prediction fields at the top level per current backend
        if response.status_code == 200:
            result = response.json()
            predicted_category = result.get("predicted_category")
            confidence = result.get("confidence")
            class_probabilities = result.get("class_probabilities", {})
            metadata = result.get("metadata", {})

            st.success(f"Predicted Insurance Premium Category: {predicted_category}")
            if confidence is not None:
                st.write("Confidence:", confidence)

            if class_probabilities:
                st.write("Class Probabilities:")
                st.json(class_probabilities)

            if metadata:
                with st.expander("Prediction Metadata"):
                    st.json(metadata)
        else:
            st.error(f"API Error: {response.status_code}")
            # Show server-provided details if any
            try:
                st.json(response.json())
            except Exception:
                st.write(response.text)

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server. Make sure it's running on http://localhost:8000")
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")


st.caption(
    "Tip: Set environment variable FRONTEND_API_URL to point to a different API base URL."
)


