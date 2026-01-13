import asyncio
import logging
from app.services.openmeteo_provider import OpenMeteoProvider

# Configure logging to see retry attempts
logging.basicConfig(level=logging.INFO)

async def test_provider():
    provider = OpenMeteoProvider()
    print("=" * 60)
    print("TESTING OpenMeteoProvider")
    print("=" * 60)
    
    # Test 1: Real location (should work or fail with retries)
    print("\n1. Testing real location (Varese)")
    try:
        data = await provider.get_conditions(-38.0, -57.5)
        print(f"✅ Success!")
        print(f"Wind Speed: {data.wind.speed_kmh} (Should be float or None, not 0.0 if missing)")
        print(f"Wave Height: {data.waves.height_m}")
        print(f"Provider: {data.provider}")
    except Exception as e:
        print(f"❌ Failed: {e}")

    # Test 2: Invalid location/Fail scenario (to test retries manually if we could mock)
    # Since we can't easily mock network failure here without mocks, we rely on the fact 
    # that the code now has @retry and returns None.
    
    # We can inspect the code behavior by observing the output above. 
    # If Marine API fails (ocean only) but Forecast works (land), we should see mixed data.
    
if __name__ == "__main__":
    asyncio.run(test_provider())
