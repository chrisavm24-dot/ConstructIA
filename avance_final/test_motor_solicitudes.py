"""Pruebas funcionales independientes del clasificador ML y de la GPU."""
import unittest
from avance_final.motor_solicitudes import (
    analizar_solicitud,
    extraer_equipo,
    extraer_municipio,
    extraer_preferencia_operador,
    responder_orientacion,
)


class MotorSolicitudesTests(unittest.TestCase):
    def test_prioridad_precio(self):
        r = analizar_solicitud("Quiero saber el precio de una plataforma elevadora", "renta_plataforma")
        self.assertEqual(r["intencion_svm_original"], "renta_plataforma")
        self.assertEqual(r["intencion_final"], "cotizacion")
        self.assertEqual(r["equipo_mencionado"], "plataforma_elevadora")

    def test_cotizar(self):
        self.assertEqual(
            analizar_solicitud("Cotízame una retroexcavadora", "catalogo_maquinaria")["intencion_final"],
            "cotizacion",
        )

    def test_cuanto_cuesta(self):
        self.assertEqual(
            analizar_solicitud("¿Cuánto cuesta?", "catalogo_maquinaria")["intencion_final"],
            "cotizacion",
        )

    def test_intencion_no_precio(self):
        self.assertEqual(
            analizar_solicitud("Necesito una retroexcavadora", "renta_retroexcavadora")["intencion_final"],
            "renta_retroexcavadora",
        )

    def test_municipio_existente(self):
        self.assertEqual(extraer_municipio("La ocupo en Monterrey"), "Monterrey")

    def test_municipio_acentos(self):
        self.assertEqual(extraer_municipio("En San Nicolás"), "San Nicolás")

    def test_municipio_no_inventar(self):
        self.assertIsNone(extraer_municipio("En cualquier municipio"))

    def test_no_confundir_excavadora(self):
        self.assertIsNone(extraer_equipo("Necesito excavadora hidráulica"))

    def test_sin_operador(self):
        self.assertEqual(extraer_preferencia_operador("No quiero operador"), "sin operador")

    def test_con_operador(self):
        self.assertEqual(extraer_preferencia_operador("Necesito con operador"), "con operador")

    def test_pregunta_no_es_preferencia(self):
        self.assertIsNone(extraer_preferencia_operador("¿La plataforma viene sin operador?"))

    def test_conflicto_visual(self):
        r = analizar_solicitud("Quiero una retroexcavadora", "renta_retroexcavadora", "minicargador")
        self.assertTrue(r["discrepancia_texto_imagen"])
        self.assertIn("no coinciden", responder_orientacion(r))

    def test_visual_no_permitido(self):
        r = analizar_solicitud("Hola", "saludo", "grua")
        self.assertIsNone(r["equipo_sugerido_por_imagen"])

    def test_precio_no_inventado(self):
        r = analizar_solicitud("¿Cuánto cuesta la plataforma?", "renta_plataforma")
        self.assertIn("No confirmo precios", responder_orientacion(r))


if __name__ == "__main__":
    unittest.main()
