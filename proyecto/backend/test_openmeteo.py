import asyncio
import httpx

async def test_apis():
    """Test múltiples endpoints de OpenMeteo"""
    
    # Test 1: Marine API (solo para océano abierto)
    print("=" * 60)
    print("TEST 1: Marine API (océano - puede no tener viento)")
    print("=" * 60)
    url1 = "https://marine-api.open-meteo.com/v1/marine"
    params1 = {
        "latitude": -38.0,
        "longitude": -57.5,
        "hourly": "wave_height,wind_speed_10m,wind_direction_10m",
        "forecast_days": 1
    }
    
    async with httpx.AsyncClient() as client:
        resp1 = await client.get(url1, params=params1, timeout=10.0)
        data1 = resp1.json()
        if "hourly" in data1:
            hourly = data1["hourly"]
            print(f"Wave height: {hourly.get('wave_height', [])[:3]}")
            print(f"Wind speed: {hourly.get('wind_speed_10m', [])[:3]}")
            print(f"Wind direction: {hourly.get('wind_direction_10m', [])[:3]}\n")
    
    # Test 2: Weather Forecast API (para viento en tierra/costa)
    print("=" * 60)
    print("TEST 2: Weather Forecast API (viento costero - debería funcionar)")
    print("=" * 60)
    url2 = "https://api.open-meteo.com/v1/forecast"
    params2 = {
        "latitude": -38.0,
        "longitude": -57.5,
        "hourly": "wind_speed_10m,wind_direction_10m",
        "timezone": "America/Argentina/Buenos_Aires",
        "forecast_days": 1
    }
    
    async with httpx.AsyncClient() as client:
        resp2 = await client.get(url2, params=params2, timeout=10.0)
        data2 = resp2.json()
        if "hourly" in data2:
            hourly = data2["hourly"]
            print(f"Times: {hourly.get('time', [])[:3]}")
            print(f"Wind speed: {hourly.get('wind_speed_10m', [])[:3]} km/h")
            print(f"Wind direction: {hourly.get('wind_direction_10m', [])[:3]}°\n")
            
    print("=" * 60)
    print("CONCLUSIÓN:")
    print("=" * 60)
    print("Si Marine API no tiene viento pero Forecast API sí,")
    print("necesitamos combinar ambos endpoints:")
    print("  - Forecast API → viento")
    print("  - Marine API → olas")

if __name__ == "__main__":
    asyncio.run(test_apis())
