import requests
import json
from datetime import datetime, timezone

# Configuración
LAT = -38.014
LON = -57.530
TIMEZONE = "auto"
MODELS = ["best_match", "ecmwf_ifs04", "gfs_seamless"]

# Variaciones de coordenadas
TEST_POINTS = [
    {"name": "Varese (Offshore 2km)", "lat": -38.014, "lon": -57.510}, # Mar adentro
]

def audit_forecast():
    print("\n[INFO] Auditing General Forecast API (Wind Sensitivity)...")
    url = "https://api.open-meteo.com/v1/forecast"
    
    for point in TEST_POINTS:
        print(f"\n--- Testing Point: {point['name']} ---")
        for model in ["best_match", "gfs_seamless"]:
            params = {
                "latitude": point["lat"],
                "longitude": point["lon"],
                "hourly": "wind_speed_10m,wind_direction_10m,wind_gusts_10m",
                "timezone": TIMEZONE,
                "current": "wind_speed_10m,wind_direction_10m,wind_gusts_10m",
                "models": model
            }
            
            try:
                r = requests.get(url, params=params)
                r.raise_for_status()
                data = r.json()
                curr = data.get("current", {})
                
                ws = curr.get('wind_speed_10m')
                wg = curr.get('wind_gusts_10m')
                wd = curr.get('wind_direction_10m')
                
                ws_str = f"{ws:.1f}" if ws is not None else "N/A"
                wg_str = f"{wg:.1f}" if wg is not None else "N/A"
                wd_str = f"{wd}" if wd is not None else "N/A"
                
                # Print secondary vars
                temp = curr.get('temperature_2m')
                precip = curr.get('precipitation')
                uv = curr.get('uv_index')
                cloud = curr.get('cloudcover')
                
                print(f"Model: {model:15} | Wind: {ws_str:>5} km/h | Gusts: {wg_str:>5} km/h | Dir: {wd_str} deg")
                print(f"   -> Temp: {temp}C | Precip: {precip}mm | UV: {uv} | Cloud: {cloud}%")
                
            except Exception as e:
                print(f"[ERROR] with {model}: {e}")

def audit_marine():
    print("\n[INFO] Auditing Marine API...")
    url = "https://marine-api.open-meteo.com/v1/marine"
    
    # Variables a probar
    vars = "wave_height,wave_period,wave_direction"
    
    params = {
        "latitude": LAT,
        "longitude": LON,
        "hourly": vars,
        "timezone": TIMEZONE,
        "forecast_days": 1
    }
    
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        
        hourly = data.get("hourly", {})
        print(f"[OK] Status: {r.status_code}")
        
        # Tomar primer valor (hora 0)
        idx = 0
        print("\n--- Marine Conditions (First Hour) ---")
        print(f"Wave Height: {hourly.get('wave_height', [])[idx]} m")
        print(f"Wave Period: {hourly.get('wave_period', [])[idx]} s")
        print(f"Wave Direction: {hourly.get('wave_direction', [])[idx]} deg")
        
    except Exception as e:
        print(f"[ERROR] Marine API Error: {e}")

if __name__ == "__main__":
    print(f"[START] Auditoria para Lat: {LAT}, Lon: {LON}")
    audit_forecast()
    audit_marine()
