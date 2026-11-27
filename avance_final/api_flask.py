"""API REST de ConstructIA. Ejecutar: python -m avance_final.api_flask."""
from __future__ import annotations
import json
import logging
import os
import time
from uuid import uuid4

from flask import Flask, jsonify, request

from avance_final.agente import procesar
from avance_final.inferencia import ModeloNoDisponible, vision_disponible

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 9 * 1024 * 1024
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@app.before_request
def registrar_inicio():
    request.id_seguimiento = uuid4().hex[:12]
    request.inicio = time.monotonic()


@app.after_request
def registrar_fin(respuesta):
    transcurrido = int((time.monotonic() - getattr(request, "inicio", time.monotonic())) * 1000)
    respuesta.headers["X-Request-ID"] = getattr(request, "id_seguimiento", "")
    respuesta.headers["Cache-Control"] = "no-store"
    app.logger.info("id=%s metodo=%s ruta=%s codigo=%s ms=%s",
                    getattr(request, "id_seguimiento", ""), request.method,
                    request.path, respuesta.status_code, transcurrido)
    # No registrar mensajes, imágenes, nombres ni datos de contacto.
    return respuesta


@app.get("/health")
def health():
    visual = vision_disponible()
    return jsonify({
        "servicio": "ConstructIA",
        "estado": "listo" if visual else "parcial",
        "nlp": "disponible_al_solicitar",
        "vision": "disponible" if visual else "sin_pesos_entrenados",
    })


@app.post("/api/interactuar")
def interactuar():
    try:
        if request.is_json:
            carga = request.get_json(silent=True)
            if not isinstance(carga, dict):
                raise ValueError("Se espera un objeto JSON.")
            texto, estado, imagen = carga.get("texto", ""), carga.get("estado", {}), None
        else:
            texto = request.form.get("texto", "")
            estado = json.loads(request.form.get("estado", "{}"))
            archivo = request.files.get("imagen")
            imagen = archivo.read() if archivo is not None else None
        if not isinstance(estado, dict):
            raise ValueError("El estado debe ser un objeto JSON.")
        resultado = procesar(texto, estado, imagen)
        return jsonify(resultado)
    except (ValueError, json.JSONDecodeError) as exc:
        return jsonify({"error": str(exc), "tipo": "entrada_invalida"}), 400
    except ModeloNoDisponible as exc:
        return jsonify({"error": str(exc), "tipo": "modelo_visual_no_disponible"}), 503
    except Exception:
        app.logger.exception("Error interno id=%s", getattr(request, "id_seguimiento", "?"))
        return jsonify({
            "error": "La solicitud no pudo procesarse. Intenta de nuevo o consulta al administrador.",
            "tipo": "error_interno",
        }), 500


@app.errorhandler(413)
def archivo_grande(_):
    return jsonify({"error": "La solicitud excede el límite permitido.", "tipo": "archivo_grande"}), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
