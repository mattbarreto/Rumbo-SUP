import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="proyecto/backend/.env")

async def test_apis():
    print("🌊 Iniciando diagnóstico de APIs de clima...\n")
    
    # --- 1. Test OpenMeteo ---
    print("1️⃣ Probando OpenMeteo (Gratuito, sin key)...")
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": -38.00,
            "longitude": -57.53,
            "hourly": "wind_speed_10m",
            "timezone": "America/Argentina/Buenos_Aires"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=10.0)
            if resp.status_code == 200:
                data = resp.json()
                ws = data.get("hourly", {}).get("wind_speed_10m", [])[0]
                print(f"✅ OpenMeteo OK! Viento actual: {ws} km/h")
            else:
                print(f"❌ OpenMeteo Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ OpenMeteo Exception: {e}")

    print("   ...Reintentando con requests síncrono...")
    try:
        import requests
        resp = requests.get(url, params=params, timeout=10)
        print(f"   Requests Status: {resp.status_code}")
        if resp.ok:
            print("   ✅ Requests OK!")
        else:
            print(f"   ❌ Requests Error: {resp.text}")
    except Exception as e:
        print(f"   ❌ Requests Exception: {e}")

    # --- 2. Test Stormglass ---
    print("\n2️⃣ Probando Stormglass (Requiere API Key)...")
    key = os.getenv("STORMGLASS_API_KEY")
    if not key:
        print("⚠️ No se encontró STORMGLASS_API_KEY en .env")
    else:
        try:
            url = "https://api.stormglass.io/v2/weather/point"
            params = {
                "lat": -38.00,
                "lng": -57.53,
                "params": "windSpeed",
                "source": "sg"
            }
            headers = {"Authorization": key}
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, params=params, headers=headers, timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json()
                    ws = data.get("hours", [])[0].get("windSpeed", {}).get("sg")
                    print(f"✅ Stormglass OK! Viento: {ws} m/s")
                elif resp.status_code == 402:
                    print("❌ Stormglass: Quota Exceeded (Límite diario alcanzado)")
                else:
                    print(f"❌ Stormglass Error: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"❌ Stormglass Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_apis())
