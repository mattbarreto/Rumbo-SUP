import httpx
import asyncio

async def test_health_only():
    """Test simple del health endpoint"""
    try:
        url = "http://localhost:8000/api/health"
        print(f"Testing: {url}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("\n✅ Backend está corriendo correctamente")
                return True
            else:
                print(f"\n❌ Backend devolvió status {response.status_code}")
                return False
                
    except httpx.ConnectError:
        print("❌ No se puede conectar al backend")
        print("Verificá que esté corriendo en http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_health_only())
