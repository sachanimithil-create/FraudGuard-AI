import joblib
import pandas as pd

# Load trained model
MODEL_PATH = "models/fraud_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_transaction(data: dict):
    """
    Predict whether a transaction is Fraud or Genuine.

    Parameters:
        data (dict): Transaction features.

    Returns:
        int: Prediction (0 = Genuine, 1 = Fraud)
    """

    input_df = pd.DataFrame([data])

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0][1]

    prediction_label = "Fraud" if prediction == 1 else "Genuine"

    return {
    "prediction": prediction_label,
    "fraud_probability": round(float(probability), 8)
     }