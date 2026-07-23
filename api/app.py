from fastapi import FastAPI
from pydantic import BaseModel

from src.predict import predict_transaction

app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="Predict whether a credit card transaction is Fraud or Genuine",
    version="1.0"
)

# Request Body
class Transaction(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float


@app.get("/")
def home():
    return {
        "message": "Credit Card Fraud Detection API is Running"
    }

@app.post("/predict")
def predict(data: Transaction):

    result = predict_transaction(data.model_dump())

    return result