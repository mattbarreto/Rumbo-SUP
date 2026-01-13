import httpx
import asyncio

async def test_render_production():
    """Test del servidor de producción en Render.com"""
    
    url = "https://rumbo-sup-backend.onrender.com/api/timeline"
    
    payload = {
        "spot_id": "varese",
        "user": {
            "board_type": "inflable",
            "experience": "beginner",
            "paddle_power": "medium",
            "session_goal": "calma"
        }
    }
    
    print("=" * 70)
    print("🌐 TESTING PRODUCCIÓN EN RENDER.COM")
    print("=" * 70)
    print(f"URL: {url}\n")
    
    try:
        async with httpx.AsyncClient() as client:
            print("⏳ Enviando request (puede tardar si cold start)...")
            response = await client.post(url, json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            
        print("✅ RESPUESTA DE PRODUCCIÓN EXITOSA!\n")
        
        if "timeline" in data and len(data["timeline"]) > 0:
            current = data["timeline"][0]
            weather = current.get("weather", {})
            wind = weather.get("wind", {})
            waves = weather.get("waves", {})
            
            wind_speed = wind.get('speed_kmh', 0)
            wave_height = waves.get('height_m', 0)
            
            print("📊 DATOS DE PRODUCCIÓN:")
            print(f"🌬️  Viento: {wind_speed:.1f} km/h")
            print(f"🌊 Olas: {wave_height:.2f} m")
            print(f"📡 Provider: {weather.get('provider', 'N/A')}")
            
            if wind_speed > 0 or wave_height > 0:
                print("\n✅ PRODUCCIÓN TIENE DATOS REALES!")
            else:
                print("\n❌ Producción aún muestra ceros")
                
    except httpx.TimeoutException:
        print("⏱️  Timeout - Render puede estar despertando (cold start)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_render_production())
