import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const fetchLiveForecast = async (lat = 6.9271, lon = 79.8612) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/predict-live`, {
      params: { lat, lon },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching forecast data", error);
    return null;
  }
};
