# Spots de SUP en Mar del Plata

SPOTS = {
    "varese": {
        "name": "Varese",
        "lat": -38.014,
        "lon": -57.530,
        "orientation_costa_deg": 90,  # Costa mira al Este
        "reglas_especificas": [
            {
                "condition": "tide_falling_and_wind_offshore",
                "flag": "deriva_varese",
                "descripcion": "Marea bajando + viento del oeste puede alejarte de la costa"
            }
        ],
        "visual_checklist": [
            "Mirá las olas cerca de la costa: ¿rompen de forma consistente?",
            "Observá la espuma: ¿se desplaza rápido hacia el mar (offshore) o hacia la playa (onshore)?",
            "Revisá las banderas: ¿están estiradas por el viento?"
        ]
    }
}

# Coordenadas de referencia para validar ubicación en Mar del Plata
MDQ_CENTER = {
    "lat": -38.0055,
    "lon": -57.5426,
    "max_distance_km": 50  # Radio máximo desde el centro
}
