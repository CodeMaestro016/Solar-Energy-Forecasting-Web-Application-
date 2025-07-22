import requests
import pandas as pd
import torch

def fetch_weather_from_open_meteo(lat=28.6139, lon=77.2090):
    """Fetch the past 48 hourly data for temperature, humidity, wind, and solar radiation."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,"
        f"wind_speed_10m,shortwave_radiation&past_days=2&timezone=auto"
    )

    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data['hourly'])
    df['time'] = pd.to_datetime(df['time'])

    df = df.rename(columns={
        'temperature_2m': 'Temperature (C)',
        'relative_humidity_2m': 'Humidity',
        'wind_speed_10m': 'Wind Speed (km/h)',
        'shortwave_radiation': 'Visibility (km)'  # stand-in for GHI
    })

    df = df[['Temperature (C)', 'Humidity', 'Wind Speed (km/h)', 'Visibility (km)']]
    df = df.dropna().tail(48)  # keep latest 48 time steps

    return df

def preprocess_input(df, scaler):
    """Scale and reshape input for model."""
    scaled = scaler.transform(df)
    tensor = torch.tensor(scaled, dtype=torch.float32).unsqueeze(0)
    return tensor
