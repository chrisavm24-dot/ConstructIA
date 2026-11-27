"""Pruebas HTTP Flask sin descargar modelos pesados ni inventar inferencias."""
import json
import unittest
from unittest.mock import patch

from avance_final.api_flask import app
from avance_final.inferencia import ModeloNoDisponible


class ApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.cliente = app.test_client()

    def test_health_no_inventa_modelo(self):
        with patch("avance_final.api_flask.vision_disponible", return_value=False):
            r = self.cliente.get("/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["vision"], "sin_pesos_entrenados")

    @patch("avance_final.agente.clasificar_texto", return_value="renta_plataforma")
    def test_consulta_json_y_cotizacion(self, _):
        r = self.cliente.post("/api/interactuar", json={
            "texto": "¿Cuál es el precio de una plataforma elevadora en Monterrey?",
            "estado": {},
        })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["intencion_final"], "cotizacion")
        self.assertEqual(r.json["informacion_detectada"]["municipio"], "Monterrey")
        self.assertIn("X-Request-ID", r.headers)

    def test_texto_vacio_error_400(self):
        r = self.cliente.post("/api/interactuar", json={"texto": " "})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json["tipo"], "entrada_invalida")

    def test_entrada_estado_invalido(self):
        r = self.cliente.post("/api/interactuar", json={"texto": "Hola", "estado": []})
        self.assertEqual(r.status_code, 400)

    @patch("avance_final.agente.clasificar_imagen",
           side_effect=ModeloNoDisponible("No hay checkpoint"))
    def test_modelo_visual_faltante_503(self, _):
        from io import BytesIO
        r = self.cliente.post(
            "/api/interactuar",
            data={"texto": "Qué máquina es", "estado": json.dumps({}),
                  "imagen": (BytesIO(b"imagen de ejemplo"), "maquina.jpg")},
            content_type="multipart/form-data",
        )
        self.assertEqual(r.status_code, 503)
        self.assertEqual(r.json["tipo"], "modelo_visual_no_disponible")


if __name__ == "__main__":
    unittest.main()
