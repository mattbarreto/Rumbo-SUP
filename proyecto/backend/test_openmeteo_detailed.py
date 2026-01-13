"""
Test directo de las APIs de OpenMeteo para debuggear
"""
import httpx
import asyncio
import json

async def test_forecast_api():
    """Test Forecast API (viento)"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -38.0,
        "longitude": -57.5,
        "hourly": "wind_speed_10m,wind_direction_10m",
        "timezone": "America/Argentina/Buenos_Aires",
        "forecast_days": 1
    }
    
    print("=" * 70)
    print("TEST 1: Weather Forecast API (Viento)")
    print("=" * 70)
    print(f"URL: {url}")
    print(f"Params: {json.dumps(params, indent=2)}\n")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=15.0)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                hourly = data.get("hourly", {})
                
                times = hourly.get("time", [])
                wind_speeds = hourly.get("wind_speed_10m", [])
                wind_dirs = hourly.get("wind_direction_10m", [])
                
                print(f"✅ API respondió correctamente")
                print(f"Total horas: {len(times)}")
                print(f"\nPrimeras 3 horas:")
                for i in range(min(3, len(times))):
                    print(f"  {times[i]} → {wind_speeds[i]} km/h @ {wind_dirs[i]}°")
                    
                if all(s is None for s in wind_speeds[:5]):
                    print("\n⚠️  WARNING: Todos los valores de viento son None")
                elif all(s == 0 for s in wind_speeds[:5] if s is not None):
                    print("\n⚠️  WARNING: Todos los valores de viento son 0")
                else:
                    print("\n✅ Datos de viento OK (no todos None/0)")
                    
            else:
                print(f"❌ Error HTTP {response.status_code}")
                print(response.text)
                
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

async def test_marine_api():
    """Test Marine API (olas)"""
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": -38.0,
        "longitude": -57.5,
        "hourly": "wave_height",
        "timezone": "America/Argentina/Buenos_Aires",
        "forecast_days": 1
    }
    
    print("\n" + "=" * 70)
    print("TEST 2: Marine API (Olas)")
    print("=" * 70)
    print(f"URL: {url}")
    print(f"Params: {json.dumps(params, indent=2)}\n")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=15.0)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                hourly = data.get("hourly", {})
                
                times = hourly.get("time", [])
                wave_heights = hourly.get("wave_height", [])
                
                print(f"✅ API respondió correctamente")
                print(f"Total horas: {len(times)}")
                print(f"\nPrimeras 3 horas:")
                for i in range(min(3, len(times))):
                    print(f"  {times[i]} → {wave_heights[i]} m")
                    
                if all(h is None for h in wave_heights[:5]):
                    print("\n⚠️  WARNING: Todos los valores de olas son None")
                elif all(h == 0 for h in wave_heights[:5] if h is not None):
                    print("\n⚠️  WARNING: Todos los valores de olas son 0")
                else:
                    print("\n✅ Datos de olas OK")
                    
            else:
                print(f"❌ Error HTTP {response.status_code}")
                print(response.text)
                
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

async def main():
    await test_forecast_api()
    await test_marine_api()
    
    print("\n" + "=" * 70)
    print("CONCLUSIÓN")
    print("=" * 70)
    print("Si ambas APIs responden con datos, el problema está en el código")
    print("Si las APIs fallan, es un problema de red/configuración")

if __name__ == "__main__":
    asyncio.run(main())
