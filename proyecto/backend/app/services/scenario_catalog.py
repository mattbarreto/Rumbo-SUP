"""
Catálogo de Escenarios Físicos para SUP (HAX v6)

Cada escenario es un "paquete pedagógico coherente" donde:
- driver, behavior, body, risk, visuals, strategy están ALINEADOS
- Incluye "qué NO hacer" y tips por nivel
- Incluye cierre pedagógico (qué practicás hoy)

El motor ya no genera piezas sueltas.
Genera un ESCENARIO que dicta todo lo demás.
"""

from typing import List, NamedTuple, Dict

class ScenarioOutput(NamedTuple):
    """Output humano del escenario - micro-narrativas completas"""
    id: str
    driver_desc: str         # Qué está moviendo el agua
    behavior_desc: str       # Cómo se ve la superficie
    body_desc: str           # Qué vas a sentir en el cuerpo
    risk_desc: str           # El riesgo de hoy y por qué
    avoid_desc: str          # Qué NO hacer hoy
    visual_cues: List[str]   # Qué buscar con los ojos
    strategy_desc: str       # Tu plan para hoy
    beginner_tip: str        # Consejo específico para principiantes
    advanced_tip: str        # Consejo específico para avanzados
    learning_focus: str      # Cierre pedagógico - qué practicás hoy


# Glosario de términos para tooltips en la UI
GLOSSARY: Dict[str, str] = {
    "serie": "Grupo de olas donde suele haber una más grande que las demás",
    "corderitos": "Pequeñas crestas blancas que aparecen cuando el viento pica el agua",
    "offshore": "Viento que sopla desde la tierra hacia el mar",
    "onshore": "Viento que sopla desde el mar hacia la costa",
    "swell": "Oleaje de fondo que llega de lejos, generado por tormentas distantes",
    "deriva": "Movimiento lateral causado por corriente o viento",
    "rompiente": "Zona donde las olas rompen al llegar a aguas poco profundas"
}


SCENARIOS = {
    
    # ───────────────────────────────────────────────────────────────
    # ESCENARIO: Mar en calma total
    # ───────────────────────────────────────────────────────────────
    "mar_plancho": ScenarioOutput(
        id="mar_plancho",
        driver_desc="Hoy casi nada está moviendo el agua. No hay viento y la marea está tranquila. El mar está haciendo una pausa.",
        behavior_desc="Vas a ver la superficie lisa como un espejo. Probablemente puedas ver el reflejo de las nubes en el agua.",
        body_desc="Tu cuerpo va a estar muy relajado. La remada va a ser suave y eficiente, casi sin esfuerzo. Podés concentrarte en la técnica sin distracciones.",
        risk_desc="El riesgo hoy es la confianza excesiva. Como todo parece fácil, podés alejarte demasiado sin darte cuenta. También ojo con el frío si te quedás quieto.",
        avoid_desc="No te vayas muy lejos solo porque parece fácil. Evitá quedarte parado sin moverte mucho tiempo (te enfriás rápido).",
        visual_cues=[
            "Superficie espejada, sin corderitos blancos",
            "Las banderas cuelgan sin moverse",
            "Podés ver el fondo cerca de la orilla"
        ],
        strategy_desc="Aprovechá para explorar zonas nuevas, pero mantené la costa siempre visible. Cada 10 minutos mirá dónde estás.",
        beginner_tip="Es un día ideal para practicar. Quedate cerca de la orilla y trabajá tu técnica de remada.",
        advanced_tip="Podés remar más largo y trabajar distancia. Aprovechá para probar técnicas nuevas.",
        learning_focus="Si el mar se ve así de calmo y lográs mantener buena técnica, es una excelente sesión para ganar confianza."
    ),
    
    # ───────────────────────────────────────────────────────────────
    # ESCENARIO: Mar movido por marea (sin viento)
    # ───────────────────────────────────────────────────────────────
    "marea_activa": ScenarioOutput(
        id="marea_activa",
        driver_desc="La marea está moviendo grandes masas de agua, pero no hay viento. El agua tiene su propia corriente interna.",
        behavior_desc="Vas a ver el agua en movimiento constante pero sin olas rompiendo. Como si el mar estuviera respirando lento.",
        body_desc="Tu core va a estar trabajando todo el tiempo para mantener el equilibrio. No es agotador, pero no vas a poder relajarte del todo. Las piernas hacen mini ajustes constantes.",
        risk_desc="La marea crea corrientes suaves que mueven tu tabla sin que lo notes. Si te quedás quieto, en 5 minutos capaz ya no estás donde empezaste.",
        avoid_desc="No te quedes parado en un lugar asumiendo que no te movés. Evitá dar la espalda a la costa por mucho tiempo.",
        visual_cues=[
            "Espuma moviéndose en diagonal, no solo hacia la orilla",
            "Objetos flotando que se desplazan solos",
            "Boyas inclinadas en una dirección"
        ],
        strategy_desc="Elegí un punto de referencia en la costa y chequeá tu posición cada 5 minutos. Si estás derivando, corregí remando hacia ese punto.",
        beginner_tip="Quedate bien cerca de la orilla. Practicá notar cuándo te movés sin querer.",
        advanced_tip="Aprovechá para practicar remada de corrección y navegación con puntos de referencia.",
        learning_focus="Si al final de la sesión pudiste mantener tu posición controlando la deriva, estás leyendo el mar correctamente."
    ),
    
    # ───────────────────────────────────────────────────────────────
    # ESCENARIO: Viento offshore (PELIGROSO)
    # ───────────────────────────────────────────────────────────────
    "viento_offshore": ScenarioOutput(
        id="viento_offshore",
        driver_desc="El viento sopla desde la tierra hacia el mar. Te va a empujar constantemente hacia adentro, y volver va a costar mucho más que salir.",
        behavior_desc="La superficie se ve engañosamente calma cerca de la orilla porque el viento aplana las olas. Pero más adentro la cosa cambia.",
        body_desc="Salir va a ser muy fácil, casi sin esfuerzo. Pero cada metro que avances lo vas a pagar doble cuando quieras volver. Los brazos se van a cansar rápido en la vuelta.",
        risk_desc="Este es el escenario más peligroso para SUP. El viento te aleja sin que te des cuenta, y cuando querés volver ya gastaste la mitad de la energía. La gente se pierde así.",
        avoid_desc="NO remes hacia adentro. Evitá alejarte más de 50 metros de la orilla. Si sentís que avanzás muy fácil, es señal de peligro, no de que estás remando bien.",
        visual_cues=[
            "Banderas apuntando hacia el mar",
            "El pelo se te va hacia adelante cuando mirás al agua",
            "Cerca parece tranquilo, pero más lejos hay corderitos"
        ],
        strategy_desc="Hoy remá siempre paralelo a la costa, nunca hacia adentro. Si sentís que avanzás muy fácil hacia el mar, VOLVÉ inmediatamente.",
        beginner_tip="Hoy mejor no salir, o quedate donde hacés pie. Este escenario es peligroso para cualquier nivel.",
        advanced_tip="Podés salir, pero con mucha precaución. Nunca más de 50m de la orilla, y siempre con alguien mirándote desde la playa.",
        learning_focus="Si lográs identificar este viento antes de entrar y decidís no alejarte, ya aprendiste algo importante sobre seguridad."
    ),
    
    # ───────────────────────────────────────────────────────────────
    # ESCENARIO: Viento onshore (cansador pero seguro)
    # ───────────────────────────────────────────────────────────────
    "viento_onshore": ScenarioOutput(
        id="viento_onshore",
        driver_desc="El viento sopla desde el mar hacia la costa. Te empuja hacia la playa, así que volver es fácil pero salir cuesta.",
        behavior_desc="Vas a ver el agua con textura, pequeños corderitos blancos, y las olas llegando más seguidas y empinadas.",
        body_desc="Salir va a exigir trabajo de brazos constante. Lo bueno es que volver es descanso. Tus hombros y espalda van a sentir la sesión.",
        risk_desc="El riesgo es cansarte demasiado yendo contra el viento. Si gastás toda la energía lejos, aunque volver sea fácil, podés quedar exhausto.",
        avoid_desc="No gastes toda tu energía en la ida. Evitá ir más lejos de lo que podrías volver remando duro si el viento aumenta.",
        visual_cues=[
            "Banderas apuntando hacia la playa",
            "Corderitos blancos en las crestas",
            "Las olas rompen más cerca de lo normal"
        ],
        strategy_desc="Salí contra el viento primero, cuando tenés más energía. Así la vuelta es un paseo. Guardá siempre un poco de reserva.",
        beginner_tip="Si te cuesta mucho salir, no fuerces. Es mejor una sesión corta cerca de la orilla.",
        advanced_tip="Es buen día para trabajar potencia de remada. Usá el viento como resistencia de entrenamiento.",
        learning_focus="Si lográs dosificar tu energía y volver sin agotarte, estás entendiendo cómo manejar el viento."
    ),
    
    # ───────────────────────────────────────────────────────────────
    # ESCENARIO: Viento cruzado (deriva lateral)
    # ───────────────────────────────────────────────────────────────
    "viento_cross": ScenarioOutput(
        id="viento_cross",
        driver_desc="El viento sopla paralelo a la costa, empujándote de costado. El agua se mueve en diagonal.",
        behavior_desc="Vas a ver olas que no vienen de frente sino en ángulo. La superficie tiene textura irregular.",
        body_desc="Tu core va a trabajar todo el tiempo para no caerte hacia un lado. Es como surfear permanentemente una mini ola lateral. Los pies nunca descansan.",
        risk_desc="Vas a derivar hacia un costado sin darte cuenta. Si empezás frente al club y no corregís, podés terminar 200 metros más allá en 15 minutos.",
        avoid_desc="No asumas que te movés en línea recta. Evitá alejarte de la zona vigilada o de tu punto de entrada.",
        visual_cues=[
            "Banderas en diagonal a la costa",
            "Las olas llegan en ángulo, no de frente",
            "Otros SUPs se mueven todos en la misma dirección"
        ],
        strategy_desc="Elegí dos puntos de referencia en la costa y chequeá que seguís entre ellos. Si te vas hacia un lado, corregí activamente.",
        beginner_tip="Quedate muy cerca de la orilla para poder volver fácilmente si derivás demasiado.",
        advanced_tip="Practicá navegación activa. Intentá mantener una línea recta contra la deriva.",
        learning_focus="Si al final de la sesión terminaste cerca de donde empezaste, estás leyendo la deriva correctamente."
    ),
    
    # ───────────────────────────────────────────────────────────────
    # ESCENARIO: Swell grande (oleaje de fondo)
    # ───────────────────────────────────────────────────────────────
    "swell_grande": ScenarioOutput(
        id="swell_grande",
        driver_desc="Hay olas grandes que vienen de lejos, pero acá no hay viento. Es oleaje de fondo que trae energía de una tormenta lejana.",
        behavior_desc="Vas a ver líneas de olas parejas llegando desde el horizonte. Suben y bajan con ritmo, como montañas de agua en cámara lenta.",
        body_desc="Las piernas van a estar flexionadas todo el tiempo, absorbiendo las subidas y bajadas. Es como hacer mini sentadillas constantes. El equilibrio es rítmico.",
        risk_desc="Las olas pueden tirarte si no las ves venir. Cada tanto viene una más grande que las demás (la serie). Si te agarra de costado, caés.",
        avoid_desc="No le des la espalda al horizonte. Evitá entrar justo después de que pasa una ola grande, porque suele venir otra. Nunca enfrentés las olas de costado.",
        visual_cues=[
            "Líneas paralelas de olas en el horizonte",
            "Cada 5-7 olas viene una más grande (la serie)",
            "La rompiente está más afuera de lo normal"
        ],
        strategy_desc="Mirá siempre hacia el horizonte para ver qué viene. Si ves una serie grande, enfrentala de frente, nunca de costado. Mejor quedarse donde no rompen.",
        beginner_tip="Hoy mejor quedarse en agua calma o no entrar. Las olas grandes requieren experiencia para manejarlas.",
        advanced_tip="Aprovechá para practicar lectura de series y timing de entrada. Es día de aprender a surfear el swell.",
        learning_focus="Si lográs anticipar las olas grandes antes de que lleguen, estás desarrollando el ojo para leer el mar."
    ),
    
    # ───────────────────────────────────────────────────────────────
    # ESCENARIO: Condiciones combinadas
    # ───────────────────────────────────────────────────────────────
    "combinado_activo": ScenarioOutput(
        id="combinado_activo",
        driver_desc="Hoy hay viento y oleaje juntos. El mar está activo desde varios lados. Es un día exigente.",
        behavior_desc="Superficie desordenada, olas que vienen de distintos ángulos. Hay textura en todas partes, corderitos, y movimiento constante.",
        body_desc="Todo el cuerpo trabaja: piernas para las olas, core para el viento, brazos para avanzar. Es un entrenamiento completo. Vas a terminar cansado pero satisfecho.",
        risk_desc="El riesgo es no poder volver si te cansás demasiado. A la combinación de viento y olas hay que respetarla. El mar exige atención total.",
        avoid_desc="No hagas una sesión larga. Evitá alejarte de la orilla. No subestimes cuánta energía te consume mantener el equilibrio.",
        visual_cues=[
            "Superficie con textura en todas direcciones",
            "Corderitos blancos por todos lados",
            "Las banderas se mueven activamente"
        ],
        strategy_desc="Sesión corta y cerca de la orilla. No más de 20-30 minutos. Si sentís que te cansás, volvé antes de quedarte sin reserva.",
        beginner_tip="Hoy mejor no salir. Si querés practicar, hacelo en agua que te llegue a la cintura.",
        advanced_tip="Buen día para un workout intenso. Establecé un tiempo límite y respetalo.",
        learning_focus="Si lográs mantener el control en condiciones mixtas y volvés con energía de reserva, estás gestionando bien el esfuerzo."
    ),
}


def classify_scenario(
    wind_speed: float,
    wind_rel: str,
    wave_height: float,
    tide_state: str,
    flags: List[str]
) -> str:
    """Clasifica las condiciones en UN escenario coherente."""
    
    # Safe defaults for None values
    wind_speed = wind_speed if wind_speed is not None else 0.0
    wave_height = wave_height if wave_height is not None else 0.0
    
    if "riesgo_deriva" in flags or (wind_rel == "offshore" and wind_speed > 8):
        return "viento_offshore"
    
    if wind_speed > 15 and wave_height > 0.8:
        return "combinado_activo"
    
    if wave_height > 1.0 and wind_speed < 12:
        return "swell_grande"
    
    if wind_rel == "onshore" and wind_speed > 12:
        return "viento_onshore"
    
    if wind_rel == "cross" and wind_speed > 10:
        return "viento_cross"
    
    if tide_state in ["rising", "falling"] and wind_speed < 10 and wave_height < 0.6:
        return "marea_activa"
    
    if wind_speed < 8 and wave_height < 0.4:
        return "mar_plancho"
    
    return "marea_activa"


def get_scenario(scenario_id: str) -> ScenarioOutput:
    """Retorna el escenario completo"""
    return SCENARIOS.get(scenario_id, SCENARIOS["marea_activa"])


def get_glossary_term(term: str) -> str:
    """Retorna la definición de un término del glosario"""
    return GLOSSARY.get(term.lower(), "")
