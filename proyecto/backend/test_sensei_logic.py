import sys
import os
from pprint import pprint

# Add the current directory to sys.path to make imports work
sys.path.append(os.getcwd())

from app.services.sensei_engine import SenseiEngine
from app.models.schemas import (
    WeatherData, UserProfile, WindData, WaveData, AtmosphereData, TideData
)

def create_mock_weather(
    wind_speed=10.0, wind_dir="offshore",
    wave_height=0.5, wave_period=10.0,
    uv=5.0, precip=0.0, vis=10.0, wcode=0
):
    return WeatherData(
        wind=WindData(
            speed_kmh=wind_speed,
            direction_deg=270, # West
            relative_direction=wind_dir
        ),
        waves=WaveData(
            height_m=wave_height,
            period_s=wave_period,
            direction_deg=90
        ),
        atmosphere=AtmosphereData(
            temperature_c=20,
            precipitation_mm=precip,
            cloud_cover_pct=20,
            uv_index=uv,
            visibility_km=vis,
            weather_code=wcode
        ),
        tide=TideData(state="rising"),
        timestamp="2023-10-27T10:00:00Z",
        provider="mock"
    )

def test_sensei():
    engine = SenseiEngine()
    user = UserProfile(
        board_type="inflable",
        experience="beginner",
        paddle_power="medium",
        session_goal="calma"
    )
    spot_id = "varese" # Mock spot ID

    print("=== TEST 1: Ideal Day ===")
    w1 = create_mock_weather(wind_speed=5, wave_height=0.3, wave_period=12, uv=3, precip=0)
    res1 = engine.analyze(w1, spot_id, user)
    print(f"Scores: {res1.scores}")
    print(f"Flags: {res1.flags}")
    print(f"Risk: {res1.semantics.risk_desc}")
    print("-" * 20)

    print("=== TEST 2: Dangerous Storm (Lighting) ===")
    w2 = create_mock_weather(wcode=95, vis=5) # Thunderstorm
    res2 = engine.analyze(w2, spot_id, user)
    print(f"Scores: {res2.scores}")
    print(f"Flags: {res2.flags}") # Should include 'tormenta_electrica'
    print(f"Risk: {res2.semantics.risk_desc}")
    if res2.scores.seguridad == 0:
        print("PASS: Security is 0")
    else:
        print(f"FAIL: Security is {res2.scores.seguridad}")
    print("-" * 20)

    print("=== TEST 3: Choppy Water (Short Period) ===")
    w3 = create_mock_weather(wave_height=1.0, wave_period=4.0)
    res3 = engine.analyze(w3, spot_id, user)
    print(f"Scores: {res3.scores}")
    print(f"Flags: {res3.flags}") # Should include 'mar_picado'
    print(f"Semantics (Risk): {res3.semantics.risk_desc}")
    if "mar_picado" in res3.flags:
        print("PASS: 'mar_picado' flag detected")
    else:
        print("FAIL: 'mar_picado' flag missing")
    print("-" * 20)

    print("=== TEST 4: High UV ===")
    w4 = create_mock_weather(uv=8.0)
    res4 = engine.analyze(w4, spot_id, user)
    print(f"Flags: {res4.flags}") # Should include 'uv_alto'
    print(f"Strategy: {res4.semantics.strategy_desc}")
    if "uv_alto" in res4.flags and "sol está muy fuerte" in res4.semantics.strategy_desc:
        print("PASS: UV detected and text injected")
    else:
        print("FAIL: UV logic incorrect")
    print("-" * 20)

    print("=== TEST 5: Rain ===")
    w5 = create_mock_weather(precip=2.0)
    res5 = engine.analyze(w5, spot_id, user)
    print(f"Flags: {res5.flags}")
    print(f"Risk: {res5.semantics.risk_desc}")
    if "lluvia" in res5.flags and "lluvia" in res5.semantics.risk_desc.lower():
         print("PASS: Rain detected")
    else:
         print("FAIL: Rain logic incorrect")

if __name__ == "__main__":
    test_sensei()
