import httpx
import asyncio

async def test_timeline_real_data():
    """Test timeline con datos REALES de Mar del Plata"""
    
    url = "http://localhost:8000/api/timeline"
    
    # Payload CORRECTO con valores EN INGLÉS
    payload = {
        "spot_id": "varese",
        "user": {
            "board_type": "inflable",  
            "experience": "beginner",  # beginner, intermediate, advanced
            "paddle_power": "medium",   # low, medium, high
            "session_goal": "calma"    # Este parece estar en español, lo veremos
        }
    }
    
    print("=" * 70)
    print("🌊 VERIFICANDO DATOS REALES DEL BACKEND LOCAL")
    print("=" * 70)
    print(f"📍 Spot: Varese, Mar del Plata (-38.0, -57.5)")
    print(f"🔗 URL: {url}\n")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            
        print("✅ RESPUESTA EXITOSA DEL BACKEND!\n")
        
        # Analizar primer punto (AHORA)
        if "timeline" in data and len(data["timeline"]) > 0:
            current = data["timeline"][0]
            weather = current.get("weather", {})
            result = current.get("result", {})
            wind = weather.get("wind", {})
            waves = weather.get("waves", {})
            tide = weather.get("tide", {})
            
            print("📊 DATOS METEOROLÓGICOS ACTUALES (AHORA):")
            print("-" * 70)
            print(f"⏰ Hora: {current.get('hour_label', 'N/A')}")
            print(f"🌬️  Velocidad viento: {wind.get('speed_kmh', 0):.1f} km/h")
            print(f"🧭 Dirección viento: {wind.get('direction_deg', 0)}°")
            print(f"🌊 Altura olas: {waves.get('height_m', 0):.2f} m")
            print(f"🌊 Estado marea: {tide.get('state', 'N/A').upper()}")
            print(f"📡 Provider: {weather.get('provider', 'N/A')}")
            print()
            
            print("🎯 ANÁLISIS DEL MOTOR (LAYER A - Deterministic):")
            print("-" * 70)
            safety = result.get("safety_score", 0)
            effort = result.get("effort_score", 0)
            enjoyment = result.get("enjoyment_score", 0)
            
            print(f"🛡️  Seguridad: {safety}/100")
            print(f"💪 Esfuerzo: {effort}/100")
            print(f"😊 Disfrute: {enjoyment}/100")
            print(f"⭐ Recomendación: {result.get('recommendation', 'N/A').upper()}")
            print()
            
            # VERIFICACIÓN CRÍTICA
            wind_speed = wind.get('speed_kmh', 0)
            wave_height = waves.get('height_m', 0)
            
            print("🔍 VERIFICACIÓN DE DATOS REALES:")
            print("-" * 70)
            
            if wind_speed == 0 and wave_height == 0:
                print("❌ PROBLEMA: Todos los valores están en 0")
                print("   → APIs de OpenMeteo no están devolviendo datos")
            elif wind_speed == 0:
                print("⚠️  Viento en 0 (puede ser problema de Forecast API)")
                print(f"   → Olas: {wave_height:.2f} m (OK)")
            elif wave_height == 0:
                print("⚠️  Olas en 0 (puede ser problema de Marine API)")
                print(f"   → Viento: {wind_speed:.1f} km/h (OK)")
            else:
                print("✅ ¡DATOS REALES CONFIRMADOS!")
                print(f"   ✓ Viento: {wind_speed:.1f} km/h")
                print(f"   ✓ Olas: {wave_height:.2f} m")
                print(f"   ✓ Marea: {tide.get('state', 'N/A')}")
                
            # Mostrar variabilidad en el timeline
            print()
            print("📈 PRONÓSTICO (próximas 5 horas):")
            print("-" * 70)
            
            wind_values = []
            wave_values = []
            
            for i, point in enumerate(data["timeline"][:5]):
                hour = point.get('hour_label', 'N/A')
                w = point.get('weather', {})
                wind_val = w.get('wind', {}).get('speed_kmh', 0)
                wave_val = w.get('waves', {}).get('height_m', 0)
                safety_val = point.get('result', {}).get('safety_score', 0)
                
                wind_values.append(wind_val)
                wave_values.append(wave_val)
                
                print(f"{hour:>5} → Viento: {wind_val:5.1f} km/h | Olas: {wave_val:4.2f} m | Seguridad: {safety_val:3d}/100")
            
            # Verificar que haya variación
            wind_varies = len(set(wind_values)) > 1
            wave_varies = len(set(wave_values)) > 1
            
            print()
            print("🔄 VERIFICACIÓN DE VARIABILIDAD:")
            print("-" * 70)
            if wind_varies:
                print("✅ Viento VARÍA en el tiempo (datos reales)")
            else:
                print("⚠️  Viento NO varía (puede ser estático)")
                
            if wave_varies:
                print("✅ Olas VARÍAN en el tiempo (datos reales)")
            else:
                print("⚠️  Olas NO varían (puede ser estático)")
                
        else:
            print("❌ No se encontraron datos en el timeline")
            
    except httpx.HTTPStatusError as e:
        print(f"❌ Error HTTP {e.response.status_code}")
        error_detail = e.response.json()
        if "detail" in error_detail:
            print("\nDetalles del error de validación:")
            for err in error_detail["detail"]:
                print(f"  - Campo: {err.get('loc', 'N/A')}")
                print(f"    Mensaje: {err.get('msg', 'N/A')}")
                print(f"    Esperado: {err.get('ctx', {}).get('expected', 'N/A')}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_timeline_real_data())
