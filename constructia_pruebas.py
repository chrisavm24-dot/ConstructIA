from constructia_reglas import identificar_intencion
from constructia_chatbot import ConstructIA

# Escenarios independientes, ficticios y repetibles. Cada caso comienza con bot nuevo.
CASOS_PRUEBA = [
    ("01 Saludo", ["Hola"]),
    ("02 Servicios de construcción", ["¿Qué servicios de construcción ofrecen?"]),
    ("03 Solicitud de obra completa", ["Quiero construir una bodega", "Bodega de almacenamiento", "Guadalupe", "10 x 8 metros", "15 de noviembre", "Cliente Demo / demo@example.com"]),
    ("04 Catálogo", ["¿Qué maquinaria rentan?"]),
    ("05 Retroexcavadora completa", ["Necesito una retroexcavadora", "Santiago", "15 de noviembre", "3 días", "Con operador", "Contacto Prueba / demo@example.com"]),
    ("06 Plataforma completa", ["Busco una plataforma elevadora", "Monterrey", "18 de noviembre", "2 días", "Sin operador", "Cliente Ejemplo / demo@example.com"]),
    ("07 Minicargador", ["¿Rentan minicargadores?", "Apodaca", "20 de noviembre", "4 días", "Sin operador", "Contacto Demo / demo@example.com"]),
    ("08 Cotización", ["¿Cuánto cuesta rentar?"]),
    ("09 Disponibilidad", ["¿Tienen disponibilidad para mañana?"]),
    ("10 Requisitos", ["¿Qué requisitos piden?"]),
    ("11 Operador", ["¿Incluye operador?"]),
    ("12 Contacto", ["Quiero hablar con un asesor"]),
    ("13 Cobertura", ["¿Qué municipios cubren?"]),
    ("14 Agradecimiento", ["Muchas gracias"]),
    ("15 Despedida", ["Adiós"]),
    ("16 Consulta fuera de alcance", ["¿Venden boletos de avión?"]),
    ("17 Mensaje combinado", ["Hola, necesito rentar una retroexcavadora", "Escobedo", "21 de noviembre", "1 día", "Con operador", "Cliente Ficticio / demo@example.com"]),
    ("18 Cancelación", ["Quiero remodelar mi casa", "cancelar"]),
]

# Para ejecutar automáticamente y conservar pruebas en formato estructurado.
def ejecutar_pruebas(verbose: bool = True) -> list[dict]:
    resultados = []
    for titulo, mensajes in CASOS_PRUEBA:
        bot = ConstructIA()
        turnos = []
        for mensaje in mensajes:
            respuesta = bot.responder(mensaje)
            turnos.append({"entrada": mensaje, "intencion": bot.ultima_intencion, "respuesta": respuesta})
        resultados.append({"caso": titulo, "turnos": turnos, "ultimo_paso": bot.paso})
        if verbose:
            print("\n===", titulo, "===")
            for turno in turnos:
                print("Cliente:", turno["entrada"])
                print("Intención/paso:", turno["intencion"])
                print("ConstructIA:", turno["respuesta"])
    return resultados


def validar_reglas() -> dict[str, int]:
    controles = {
        "Hola": "saludo",
        "Quiero construir una casa": "solicitar_obra",
        "¿Qué servicios de construcción ofrecen?": "servicios_construccion",
        "¿Qué maquinaria rentan?": "catalogo_maquinaria",
        "Necesito una retroexcavadora": "renta_retroexcavadora",
        "Busco plataforma elevadora": "renta_plataforma",
        "¿Rentan minicargadores?": "renta_minicargador",
        "¿Cuánto cuesta rentar?": "cotizacion",
        "¿Tienen disponibilidad?": "disponibilidad",
        "¿Qué requisitos piden?": "requisitos",
        "¿Incluye operador?": "operador",
        "Quiero hablar con un asesor": "contacto",
        "¿Qué municipios cubren?": "zonas",
        "Muchas gracias": "agradecimiento",
        "Adiós": "despedida",
        "Hola, necesito rentar una retroexcavadora": "renta_retroexcavadora",
        "Buenas tardes, quiero construir una habitación": "solicitar_obra",
        "¿Cuánto cuesta la plataforma?": "cotizacion",
    }
    correctos = sum(identificar_intencion(msg) == esperado for msg, esperado in controles.items())
    if correctos != len(controles):
        malos = [(m, identificar_intencion(m), e) for m, e in controles.items() if identificar_intencion(m) != e]
        raise AssertionError(f"Intenciones fallidas: {malos}")
    pruebas = ejecutar_pruebas(False)
    assert len(pruebas) >= 10
    for test in pruebas:
        assert all(t["respuesta"].strip() for t in test["turnos"])
    for i in [2, 4, 5, 6, 16]:
        assert pruebas[i]["ultimo_paso"] is None, pruebas[i]["caso"]
        assert "SOLICITUD DEMO" in pruebas[i]["turnos"][-1]["respuesta"]
    assert pruebas[16]["turnos"][0]["intencion"] == "renta_retroexcavadora"
    assert pruebas[17]["turnos"][-1]["intencion"] == "cancelacion"
    return {"intenciones_verificadas": correctos, "conversaciones_ejecutadas": len(pruebas), "flujos_completados": 5}