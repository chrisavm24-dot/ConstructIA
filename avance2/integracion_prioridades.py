"""ConstructIA V3.1: reglas de negocio encima del clasificador NLP.

No modifica el clasificador SVM ni sus métricas de evaluación.
Evita que consultas explícitas sobre precio terminen en el catálogo.
"""
from __future__ import annotations

import re
import unicodedata

PATRONES_PRECIO = (
    r"\bprecios?\b",
    r"\bcostos?\b",
    r"\btarifas?\b",
    r"\bcotiz\w*\b",
    r"\bpresupuest\w*\b",
    r"\bcuanto(?:s)?\s+(?:me\s+)?(?:cuesta|vale|sale|cobran)\b",
)


def limpiar(texto: str) -> str:
    texto = str(texto).lower().strip()
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"\s+", " ", texto)


def resolver_intencion_comercial(mensaje: str, prediccion_svm: str) -> dict:
    """La intención ML queda intacta; devolvemos una decisión adicional explicable."""
    limpio = limpiar(mensaje)
    if any(re.search(patron, limpio) for patron in PATRONES_PRECIO):
        return {
            "prediccion_svm": str(prediccion_svm),
            "intencion_final": "cotizacion",
            "regla_aplicada": (
                "prioridad de precio" if prediccion_svm != "cotizacion"
                else "sin ajuste: el modelo detectó precio"
            ),
        }
    return {
        "prediccion_svm": str(prediccion_svm),
        "intencion_final": str(prediccion_svm),
        "regla_aplicada": "ninguna",
    }


def responder_texto_imagen(decision: dict, clase_visual: str) -> str:
    """Respuesta orientativa: no confirma ni modelo exacto ni disponibilidad."""
    categoria = str(clase_visual).replace("_", " ")
    if decision["intencion_final"] == "cotizacion":
        return (
            f"Identifiqué una consulta sobre precios y la fotografía parece mostrar "
            f"una {categoria}. Para cotizar, un asesor debe confirmar la máquina, "
            "la ubicación, la fecha, la duración, el operador y la disponibilidad. "
            "No puedo proporcionar una tarifa real ni reservar el equipo."
        )
    return (
        f"Identifiqué la intención «{decision['intencion_final']}» y la imagen "
        f"parece mostrar una {categoria}. Un asesor debe verificar el tipo de "
        "maquinaria y las condiciones del servicio. Esta versión no confirma "
        "disponibilidad ni realiza reservas."
    )


if __name__ == "__main__":
    assert resolver_intencion_comercial("¿Cuál es el precio?", "catalogo_maquinaria")["intencion_final"] == "cotizacion"
    assert resolver_intencion_comercial("Quiero una cotización para retroexcavadora", "renta_retroexcavadora")["intencion_final"] == "cotizacion"
    assert resolver_intencion_comercial("No quiero operador", "operador")["intencion_final"] == "operador"
    print("Pruebas de prioridad comercial correctas.")
