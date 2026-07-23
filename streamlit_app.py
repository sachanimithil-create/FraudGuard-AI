import streamlit as st
import requests
import pandas as pd
import os

# Page Config
st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="💳",
    layout="wide"
)
HISTORY_FILE = "data/predictions/predictions.csv"

def save_prediction(data):

    os.makedirs(
        "data/predictions",
        exist_ok=True
    )

    df = pd.DataFrame([data])

    if os.path.exists(HISTORY_FILE):

        old_df = pd.read_csv(HISTORY_FILE)

        df = pd.concat(
            [old_df, df],
            ignore_index=True
        )

    df.to_csv(
        HISTORY_FILE,
        index=False
    )


# Sidebar

st.sidebar.title("💳 FraudGuard AI")

st.sidebar.info(
"""
Credit Card Fraud Detection System

Model:
Tuned XGBoost

Metrics:
F1 Score: 0.836 

ROC-AUC: 0.979

Backend:
FastAPI
"""
)

# Main Title

st.title("💳 Credit Card Fraud Detection")

st.write(
"AI powered system to identify suspicious transactions."
)

# Transaction Details

st.subheader("Transaction Information")
# Sample transaction values

sample_data = {
    "Time": 406.0,
    "Amount": 149.62,
    "V1": -1.359807,
    "V2": -0.072781,
    "V3": 2.536347,
    "V4": 1.378155,
    "V5": -0.338321,
    "V6": 0.462388,
    "V7": 0.239599,
    "V8": 0.098698,
    "V9": 0.363787,
    "V10": 0.090794,
    "V11": -0.551601,
    "V12": -0.617801,
    "V13": -0.991390,
    "V14": -0.311169,
    "V15": 1.468177,
    "V16": -0.470401,
    "V17": 0.207971,
    "V18": 0.025791,
    "V19": 0.403993,
    "V20": 0.251412,
    "V21": -0.018307,
    "V22": 0.277838,
    "V23": -0.110474,
    "V24": 0.066928,
    "V25": 0.128539,
    "V26": -0.189115,
    "V27": 0.133558,
    "V28": -0.021053
}

if st.button("📌 Load Sample Transaction"):

    st.session_state.sample = sample_data
    st.rerun()

col1, col2 = st.columns(2)

with col1:

    time = st.number_input(
    "Transaction Time",
    value=st.session_state.get(
        "sample",
        {}
    ).get("Time",0.0)
)

with col2:

    amount = st.number_input(
    "Transaction Amount",
    value=st.session_state.get(
        "sample",
        {}
    ).get("Amount",100.0)
)

# Advanced Features

with st.expander("Advanced Features (V1 - V28)"):

    st.warning(
        "These are anonymized PCA features from the dataset."
    )

    features = {}

    cols = st.columns(4)

    for i in range(1,29):

        with cols[i%4]:

            features[f"V{i}"] = st.number_input(
                f"V{i}",
                value=st.session_state.get(
                 "sample",
                 {}
                ).get(
                 f"V{i}",
                    0.0
                )
            )

# Prediction

if st.button("🔍 Analyze Transaction"):

    payload = {

        "Time": time,

        **features,

        "Amount": amount

    }

    try:

        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload
        )

        if response.status_code == 200:

            result = response.json()

        else:

            st.error("Prediction failed")
            st.stop()

    except Exception:

        st.error(
            "FastAPI server is not running."
        )

        st.stop()

    st.divider()

    probability = result["fraud_probability"]

    # Risk calculation

    if probability < 0.3:
        risk = "Low Risk"

    elif probability < 0.7:
        risk = "Medium Risk"

    else:
        risk = "High Risk"

    # Prediction Result

    if result["prediction"] == "Fraud":
        st.error(
            "🚨 Fraud Transaction Detected"
        )

    else:
        st.success(
            "✅ Genuine Transaction"
        )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Fraud Probability",
            f"{probability*100:.6f}%"
        )


    with col2:

        st.metric(
            "Risk Level",
            risk
        )



    # Save Prediction History

    current_prediction = {

    "Prediction": result["prediction"],

    "Fraud Probability (%)": round(
        probability * 100,
        6
    ),

    "Risk": risk,

    "Amount": amount

    }

    save_prediction(
    current_prediction
    )

st.divider()

st.subheader("📊 Prediction History")

if os.path.exists(HISTORY_FILE):

    history_df = pd.read_csv(
        HISTORY_FILE
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

else:

    st.info(
        "No predictions yet"
    )