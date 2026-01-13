import httpx
import asyncio

async def test_endpoint():
    print("Testing POST /api/timeline locally...")
    url = "http://localhost:8000/api/timeline"
    payload = {
        "spot_id": "varese",
        "user": {
            "board_type": "rigid",
            "experience": "intermediate",
            "paddle_power": "medium",
            "session_goal": "calma"
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=30.0)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Success")
                print(response.json())
            else:
                print(f"❌ Failed: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_endpoint())
