"""ConstructIA: prototipo exploratorio de captura de solicitudes (versión futura).

No altera las métricas ni el código entregado en los avances 1 y 2.
La predicción de SVM se recibe como dato; este módulo no reentrena modelos.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Optional

MUNICIPIOS = {
    "monterrey": "Monterrey",
    "guadalupe": "Guadalupe",
    "san nicolas": "San Nicolás",
    "san pedro": "San Pedro Garza García",
    "san pedro garza garcia": "San Pedro Garza García",
    "santa catarina": "Santa Catarina",
    "apodaca": "Apodaca",
    "escobedo": "General Escobedo",
    "general escobedo": "General Escobedo",
    "santiago": "Santiago",
    "garcia": "García",
    "juarez": "Juárez",
}
EQUIPOS = {
    "retroexcavadora": ("retroexcavadora",),
    "plataforma_elevadora": ("plataforma elevadora", "plataforma de tijera", "plataforma tipo tijera"),
    "minicargador": ("minicargador", "mini cargador"),
}
EXPRESIONES_PRECIO = (
    r"\bprecios?\b", r"\bcostos?\b", r"\btarifas?\b",
    r"\bcotiza\w*\b", r"\bpresupuest\w*\b",
    r"\bcuanto\s+(?:(?:me|nos)\s+)?(?:cuesta|vale|sale|cobran)\b",
)
CLASES_VISUALES = set(EQUIPOS)


def normalizar(mensaje: str) -> str:
    texto = unicodedata.normalize("NFD", str(mensaje).lower().strip())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", texto)


def _aparece(texto: str, expresion: str) -> bool:
    return bool(re.search(r"(?<!\w)" + re.escape(expresion) + r"(?!\w)", texto))


def extraer_municipio(mensaje: str) -> Optional[str]:
    """Solo municipios configurados. No deduce cobertura comercial real."""
    texto = normalizar(mensaje)
    # Usar la coincidencia más larga primero evita 'San Pedro' frente al nombre completo.
    for variante in sorted(MUNICIPIOS, key=len, reverse=True):
        if _aparece(texto, variante):
            return MUNICIPIOS[variante]
    return None


def extraer_equipo(mensaje: str) -> Optional[str]:
    """No tratamos 'excavadora' como retroexcavadora: son equipos distintos."""
    texto = normalizar(mensaje)
    for clase, expresiones in EQUIPOS.items():
        if any(_aparece(texto, x) for x in expresiones):
            return clase
    return None


def extraer_preferencia_operador(mensaje: str) -> Optional[str]:
    """Sólo solicitudes afirmativas explícitas; preguntas no fijan preferencia."""
    texto = normalizar(mensaje)
    if "?" in texto or "¿" in texto:
        return None
    if re.search(r"\bno (?:quiero|necesito|ocupo|requiero) (?:un )?operador\b", texto):
        return "sin operador"
    if re.search(r"\b(?:quiero|necesito|ocupo|requiero|prefiero)(?:\s+la\s+maquina)?\s+sin operador\b", texto):
        return "sin operador"
    if re.search(r"\b(?:quiero|necesito|ocupo|requiero|prefiero)(?:\s+la\s+maquina)?\s+con operador\b", texto):
        return "con operador"
    return None


def analizar_solicitud(
    mensaje: str,
    intencion_svm: str,
    clase_visual: Optional[str] = None,
) -> dict:
    """Separa predicción estadística, reglas, datos detectados y contradicciones."""
    texto = normalizar(mensaje)
    precio = any(re.search(p, texto) for p in EXPRESIONES_PRECIO)
    equipo_texto = extraer_equipo(mensaje)
    equipo_visual = clase_visual if clase_visual in CLASES_VISUALES else None
    discrepancia = bool(
        equipo_texto and equipo_visual and equipo_texto != equipo_visual
    )
    return {
        "consulta": mensaje,
        "intencion_svm_original": intencion_svm,
        "intencion_final": "cotizacion" if precio else intencion_svm,
        "regla_comercial": "prioridad de cotizacion" if precio else "sin ajuste",
        "equipo_mencionado": equipo_texto,
        "equipo_sugerido_por_imagen": equipo_visual,
        "discrepancia_texto_imagen": discrepancia,
        "municipio_mencionado": extraer_municipio(mensaje),
        "operador_solicitado": extraer_preferencia_operador(mensaje),
        "pendiente_validacion_humana": True,
    }


def responder_orientacion(resultado: dict) -> str:
    """No afirma precio, existencia, reserva o identificación definitiva."""
    if resultado["discrepancia_texto_imagen"]:
        comienzo = "El equipo mencionado y la clasificación de la fotografía no coinciden; es necesario verificarlo."
    elif resultado["equipo_mencionado"] or resultado["equipo_sugerido_por_imagen"]:
        comienzo = "Identifiqué una posible categoría de maquinaria para tu consulta."
    else:
        comienzo = "Recibí tu consulta."
    if resultado["intencion_final"] == "cotizacion":
        fin = " Para elaborar una cotización hace falta confirmar equipo, ubicación, fechas, duración y operador."
    else:
        fin = " Un asesor deberá confirmar los datos y la información del servicio."
    return comienzo + fin + " No confirmo precios, inventario ni reservas."
