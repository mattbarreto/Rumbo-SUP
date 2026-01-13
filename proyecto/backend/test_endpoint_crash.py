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
            response = await client.post(url, json=payload, timeout=60.0)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Success")
                data = response.json()
                print(f"Spot: {data.get('spot')}")
                print(f"Timeline items: {len(data.get('timeline', []))}")
            else:
                print(f"❌ Failed (Status {response.status_code})")
                # Print full response body
                try:
                    error_detail = response.json()
                    print(f"Detail: {error_detail.get('detail', 'Unknown')}")
                except:
                    print(f"Raw: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_endpoint())
