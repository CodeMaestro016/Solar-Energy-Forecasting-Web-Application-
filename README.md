# 🌞 Solar Vision – AI-Powered Solar Energy Forecasting Web App

**Solar Vision** is an AI-driven web application that forecasts solar irradiance (GHI) for the next 24 hours using real-time weather data. Designed to support smart energy decisions, the app combines cutting-edge deep learning (PatchTST) with an interactive dashboard, helping users understand and plan around solar energy potential.

---

## 🚀 Features

- 🧠 **Transformer-based forecasting model (PatchTST)** for accurate multivariate time series prediction
- 🌤️ **Live weather integration** using Open-Meteo API (temperature, humidity, wind, radiation)
- ⚙️ **FastAPI backend** serving real-time solar predictions as a REST API
- 💻 **ReactJS + Tailwind CSS** frontend dashboard with hourly solar output insights
- 📈 **Power BI export** for visual analytics and historical comparisons
- 🌍 Supports dynamic location-based forecasting via latitude and longitude

---

## 🧰 Tech Stack

| Layer         | Technology                          |
|---------------|--------------------------------------|
| Model         | PatchTST (PyTorch)                  |
| Backend       | FastAPI, Pydantic, Torch, NumPy     |
| Data          | Open-Meteo API, CSV (historical)    |
| Frontend      | ReactJS, Tailwind CSS, Axios        |
| Visualization | Power BI                            |
| Dev Tools     | VS Code, Git, Python, Node.js       |

---

## 📊 How It Works

1. **Live weather data** (48 hours) is fetched using the Open-Meteo API.
2. Input is **preprocessed and scaled**, then passed to the PatchTST model.
3. The model predicts **24 future hourly GHI values**.
4. Output is returned via API and displayed in a dashboard or exported to Power BI.

---

## 📦 Installation

### 🔹 Backend (FastAPI)

```bash
git clone https://github.com/yourusername/solar-vision.git
cd solar-vision/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
