from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import torch
from app.model import load_model_and_scaler
from app.utils import preprocess_input
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# app/main.py (add below /predict endpoint)
from app.utils import fetch_weather_from_open_meteo


# Init FastAPI app
app = FastAPI(
    title="Solar Vision API",
    description="Forecasts 24-hour solar irradiance (GHI) using PatchTST model",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load Model and Scaler
model, scaler = load_model_and_scaler()


class InputData(BaseModel):
    records: List[Dict[str, float]]  # Must contain 48 records with 4 fields each



@app.post("/predict")
def predict(data: InputData):
    if len(data.records) != 48:
        raise HTTPException(status_code=400, detail="Expected exactly 48 time steps")

    try:
        # Preprocess input
        input_tensor = preprocess_input(data.records, scaler)

        # Model prediction
        with torch.no_grad():
            output = model(input_tensor)
            preds = output.numpy()[0]  # Shape: (24,)

        # Inverse transform GHI only
        dummy = np.zeros((24, 3))
        stacked = np.hstack([dummy, preds.reshape(-1, 1)])
        prediction = scaler.inverse_transform(stacked)[:, -1]

        # ✅ Fix: Clip negative GHI to zero
        prediction = np.clip(prediction, 0, None)

        return {
            "forecast_GHI": prediction.tolist()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

# app/main.py (add below /predict endpoint)
from app.utils import fetch_weather_from_open_meteo

@app.get("/predict-live")
def predict_from_live_weather(lat: float = 28.6139, lon: float = 77.2090):
    try:
        df_live = fetch_weather_from_open_meteo(lat, lon)
        if len(df_live) < 48:
            raise HTTPException(status_code=400, detail="Not enough data returned (need 48 hours)")
        
        input_tensor = preprocess_input(df_live, scaler)

        with torch.no_grad():
            output = model(input_tensor)
            preds = output.numpy()[0]

        # Inverse transform for GHI only
        dummy = np.zeros((24, 3))
        stacked = np.hstack([dummy, preds.reshape(-1, 1)])
        prediction = scaler.inverse_transform(stacked)[:, -1]

        # ✅ Fix: clip negative values to 0
        prediction = np.clip(prediction, 0, None)

        return {
            "location": {"lat": lat, "lon": lon},
            "forecast_GHI": prediction.tolist()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# uvicorn app.main:app --reload  <- run
# http://127.0.0.1:8000/docs#/