import httpx
import asyncio

async def test_production():
    """Test del frontend en producción"""
    
    # Primero verificar que la URL del frontend esté correcta
    frontend_url = "https://rumbo-sup-frontend.onrender.com"
    
    print("=" * 70)
    print("🌐 TESTING PRODUCCIÓN EN RENDER")
    print("=" * 70)
    print(f"Frontend URL: {frontend_url}\n")
    
    # Test 1: Verificar que el frontend carga
    print("Test 1: Verificando frontend...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(frontend_url, timeout=30.0, follow_redirects=True)
            print(f"✅ Frontend responde: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend error: {e}")
    
    print("\n" + "=" * 70)
    print("IMPORTANTE:")
    print("=" * 70)
    print("Para ver datos reales, abrí la app en el navegador:")
    print(f"→ {frontend_url}")
    print("\nSi en producción ves datos reales (no zeros), el problema es")
    print("SOLO tu firewall local, no el código.")

if __name__ == "__main__":
    asyncio.run(test_production())
