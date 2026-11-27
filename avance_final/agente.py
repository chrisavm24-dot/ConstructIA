"""Agente híbrido: chatbot de reglas + NLP + visión + reglas de negocio."""
from __future__ import annotations
from avance_final.motor_solicitudes import analizar_solicitud, responder_orientacion
from avance_final.inferencia import clasificar_texto, clasificar_imagen


def procesar(texto: str, estado: dict | None = None, imagen: bytes | None = None) -> dict:
    texto = str(texto).strip()
    if not texto:
        raise ValueError("Escribe una consulta antes de enviarla.")
    if len(texto) > 2000:
        raise ValueError("La consulta debe tener máximo 2000 caracteres.")

    # Restablecemos el estado explícito de conversación, sin guardarlo en servidor.
    from constructia_chatbot import ConstructIA
    chatbot = ConstructIA()
    previo = estado if isinstance(estado, dict) else {}
    paso = previo.get("paso")
    pasos_validos = {"tipo_obra", "ubicacion", "medidas", "fecha", "duracion", "operador", "contacto"}
    chatbot.paso = paso if paso in pasos_validos else None
    datos = previo.get("datos")
    chatbot.datos = {
        k: str(v)[:300] for k, v in datos.items()
        if isinstance(k, str) and isinstance(v, (str, int, float))
    } if isinstance(datos, dict) else {}

    # La visión no inventa etiqueta: el servicio lanza un error sin pesos.
    clase_visual = clasificar_imagen(imagen) if imagen is not None else None
    pred_svm = clasificar_texto(texto)
    decision = analizar_solicitud(texto, pred_svm, clase_visual)
    en_formulario = chatbot.paso is not None
    salida_chatbot = chatbot.responder(texto)

    if decision["discrepancia_texto_imagen"]:
        respuesta = responder_orientacion(decision)
    elif decision["intencion_final"] == "cotizacion" and not en_formulario:
        respuesta = responder_orientacion(decision)
    else:
        respuesta = salida_chatbot
        if clase_visual is not None:
            respuesta += (
                " La fotografía parece corresponder a "
                + clase_visual.replace("_", " ")
                + "; un asesor debe confirmar la identificación y el servicio."
            )
    return {
        "respuesta": respuesta,
        "intencion_svm": pred_svm,
        "intencion_final": decision["intencion_final"],
        "regla_aplicada": decision["regla_comercial"],
        "clase_visual": clase_visual,
        "informacion_detectada": {
            "equipo": decision["equipo_mencionado"],
            "municipio": decision["municipio_mencionado"],
            "operador": decision["operador_solicitado"],
            "discrepancia": decision["discrepancia_texto_imagen"],
        },
        "estado": {"paso": chatbot.paso, "datos": chatbot.datos},
        "advertencia": (
            "Prototipo académico. No confirma precios, disponibilidad, "
            "reservas ni idoneidad técnica del equipo."
        ),
    }
