"""
Test SUPER SIMPLE de Forecast API con timeout largo
"""
import httpx
import time

def test_sync():
    """Test síncrono simple"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -38.0,
        "longitude": -57.5,
        "hourly": "wind_speed_10m",
        "forecast_days": 1
    }
    
    print("Probando Forecast API con httpx (síncrono)...")
    print(f"URL: {url}")
    print("Timeout: 30 segundos\n")
    
    start = time.time()
    
    try:
        response = httpx.get(url, params=params, timeout=30.0)
        elapsed = time.time() - start
        
        print(f"✅ Respuesta recibida en {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            wind_speeds = data.get("hourly", {}).get("wind_speed_10m", [])
            print(f"Datos de viento (primeros 3): {wind_speeds[:3]}")
        else:
            print(f"Error: {response.text}")
            
    except httpx.TimeoutException:
        elapsed = time.time() - start
        print(f"❌ TIMEOUT después de {elapsed:.2f}s")
        print("Esto sugiere problema de red/firewall")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_sync()
