import asyncio
import os
from dotenv import load_dotenv
from app.services.pedagogy_service import PedagogyService
from app.models.schemas import UserProfile, WeatherData, EngineResult, WindData, WaveData, TideData, Scores, Categories, SemanticAnalysis

# Load env vars
load_dotenv()

async def test_sensei():
    model = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
    print(f"🧠 Probando Sensei HAX v5 con modelo: {model}")
    print("=" * 60)
    
    # 1. Mock Data: Día con marea activa (escenario "marea_activa")
    user = UserProfile(
        board_type="inflable",
        experience="intermediate",
        paddle_power="medium",
        session_goal="calma"
    )
    
    weather = WeatherData(
        wind=WindData(speed_kmh=5, direction_deg=90, relative_direction="cross"),
        waves=WaveData(height_m=0.4),
        tide=TideData(state="rising"),
        timestamp="2023-01-01T12:00:00Z",
        provider="test"
    )
    
    # 2. Engine Result HAX v5 - micro-narrativas humanas del catálogo
    semantics = SemanticAnalysis(
        scenario_id="marea_activa",
        driver_desc="La marea está moviendo grandes masas de agua, pero no hay viento. Sentís que el agua tiene su propia corriente interna.",
        behavior_desc="Vas a ver el agua en movimiento constante pero sin olas rompiendo. Como si hubiera una respiración profunda del mar.",
        body_desc="Tu core va a estar trabajando constantemente para mantener el equilibrio. No es agotador, pero no vas a poder relajarte del todo. Las piernas van a hacer micro-ajustes todo el tiempo.",
        risk_desc="La marea puede crear corrientes suaves que mueven tu tabla sin que lo notes. Si te quedás quieto, capaz que en 5 minutos ya no estás donde empezaste.",
        visual_cues=[
            "Espuma moviéndose en diagonal, no solo hacia la orilla",
            "Objetos flotando que se desplazan solos",
            "Boyas inclinadas en una dirección"
        ],
        strategy_desc="Elegí un punto de referencia en la costa y chequeá tu posición cada 5 minutos. Si estás derivando, corregí remando hacia ese punto."
    )
    
    result = EngineResult(
        scores=Scores(seguridad=85, esfuerzo=40, disfrute=75),
        categories=Categories(seguridad="alto", esfuerzo="medio", disfrute="alto"),
        flags=[],
        semantics=semantics,
        confidence="alta"
    )
    
    # 3. Generate Explanation
    service = PedagogyService()
    try:
        explanation = await service.generate_explanation(user, weather, result)
        print("\n✨ RESPUESTA DEL SENSEI:\n")
        print(explanation)
        print("\n" + "=" * 60)
        
        # Validación
        valid = service._validate_structure(explanation)
        print(f"✅ Estructura válida: {valid}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_sensei())
