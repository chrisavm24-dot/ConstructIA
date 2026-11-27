"""Pruebas del agente con modelos sustitutos: no inventan resultados ML."""
import unittest
from unittest.mock import patch

from avance_final.agente import procesar


class AgenteTests(unittest.TestCase):
    @patch("avance_final.agente.clasificar_texto", return_value="renta_plataforma")
    def test_precio_prevalece_sobre_prediccion(self, _):
        r = procesar("Quiero conocer el precio de una plataforma elevadora")
        self.assertEqual(r["intencion_svm"], "renta_plataforma")
        self.assertEqual(r["intencion_final"], "cotizacion")
        self.assertIn("confirmar", r["respuesta"])

    @patch("avance_final.agente.clasificar_texto", return_value="renta_retroexcavadora")
    def test_datos_de_ubicacion_extraidos(self, _):
        r = procesar("Necesito retroexcavadora en Monterrey")
        self.assertEqual(r["informacion_detectada"]["municipio"], "Monterrey")

    @patch("avance_final.agente.clasificar_imagen", return_value="minicargador")
    @patch("avance_final.agente.clasificar_texto", return_value="renta_retroexcavadora")
    def test_conflicto_texto_imagen(self, *_):
        r = procesar("Quiero una retroexcavadora", imagen=b"foto")
        self.assertTrue(r["informacion_detectada"]["discrepancia"])
        self.assertIn("no coinciden", r["respuesta"])

    @patch("avance_final.agente.clasificar_texto", return_value="saludo")
    def test_estado_evitamos_persistencia_en_servidor(self, _):
        r1 = procesar("Hola")
        r2 = procesar("Hola")
        self.assertEqual(r1["estado"], r2["estado"])

    def test_rechazar_texto_vacio(self):
        with self.assertRaises(ValueError):
            procesar("")

    def test_rechazar_texto_demasiado_largo(self):
        with self.assertRaises(ValueError):
            procesar("x" * 2001)


if __name__ == "__main__":
    unittest.main()
