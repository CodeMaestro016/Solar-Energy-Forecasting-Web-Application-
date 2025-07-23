import { useEffect, useState } from "react";
import { fetchLiveForecast } from "../services/api";

const LOCATIONS = [
  { name: "Delhi", lat: 28.6139, lon: 77.2090 },
  { name: "Colombo", lat: 6.9271, lon: 79.8612 },
  { name: "Dubai", lat: 25.276987, lon: 55.296249 },
  {name: "London", lat: 	51.5074, lon: 	-0.1278 }
];

export default function Dashboard() {
  const [forecast, setForecast] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(LOCATIONS[0]);
  const [isDark, setIsDark] = useState(false);

  const loadForecast = async () => {
    const data = await fetchLiveForecast(selectedLocation.lat, selectedLocation.lon);
    if (data?.forecast_GHI?.length === 24) {
      const now = new Date();
      const enriched = data.forecast_GHI.map((ghi, i) => {
        const hour = new Date(now);
        hour.setHours(now.getHours() + i + 1);
        hour.setMinutes(0, 0, 0);
        return {
          time: hour.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }),
          hour24: hour.getHours(),
          ghi,
          label: getInsightLabel(ghi),
        };
      });

      setForecast(enriched);
    }
  };

  useEffect(() => {
    loadForecast();
  }, [selectedLocation]);

  const getInsightLabel = (ghi) => {
    if (ghi < 0.5) return "No Output 🌙";
    if (ghi < 3) return "Low ☁️";
    if (ghi < 7) return "Moderate 🌤️";
    if (ghi < 12) return "High ☀️";
    return "Very High 🔆";
  };

  return (
    <div className={`${isDark ? 'dark' : ''}`}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6 text-gray-800 dark:text-gray-100">
        
        {/* HEADER */}
        <header className="bg-white dark:bg-gray-800 shadow rounded-xl p-6 mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🌞</span>
            <div>
              <h1 className="text-2xl font-bold">Solar Vision Dashboard</h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">24-hour Solar Forecast (GHI)</p>
            </div>
          </div>

          <div className="mt-4 sm:mt-0 flex flex-col sm:flex-row gap-4 items-center">
            <select
              className="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-md border border-gray-300 dark:border-gray-600 text-sm"
              value={selectedLocation.name}
              onChange={(e) =>
                setSelectedLocation(LOCATIONS.find(loc => loc.name === e.target.value))
              }
            >
              {LOCATIONS.map(loc => (
                <option key={loc.name} value={loc.name}>{loc.name}</option>
              ))}
            </select>

            <button
              onClick={loadForecast}
              className="px-4 py-1 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm"
            >
              🔄 Refresh
            </button>

            <button
              onClick={() => setIsDark(prev => !prev)}
              className="px-3 py-1 border border-gray-400 dark:border-gray-600 rounded-md text-sm"
            >
              {isDark ? '☀️ Light Mode' : '🌙 Dark Mode'}
            </button>
          </div>
        </header>

        {/* FORECAST TABLE */}
        {forecast.length > 0 ? (
          <div className="grid grid-cols-3 gap-4 bg-white dark:bg-gray-800 p-4 rounded-xl shadow text-sm font-medium">
            <div className="font-bold text-gray-600 dark:text-gray-300">Hour</div>
            <div className="font-bold text-gray-600 dark:text-gray-300">Forecast GHI</div>
            <div className="font-bold text-gray-600 dark:text-gray-300">Solar Potential</div>

            {forecast.map((item, index) => (
              <div key={index} className="contents">
                <div className="text-gray-700 dark:text-gray-200">{item.time}</div>
                <div className="text-blue-600 dark:text-blue-300">{item.ghi.toFixed(2)}</div>
                <div className="text-green-700 dark:text-green-300">{item.label}</div>
              </div>
            ))}
          </div>
        ) : (
          <p>Loading forecast...</p>
        )}
      </div>
    </div>
  );
}
