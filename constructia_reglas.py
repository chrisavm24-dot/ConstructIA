"""ConstructIA v2 | Avance 1 - Desarrollo de Aplicaciones con IA.
Chatbot didáctico basado en reglas con Python 3.10+ y NLTK.
No conecta proveedores ni almacena solicitudes de forma persistente.
"""
from __future__ import annotations
import re
import sys
import unicodedata
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer

if sys.version_info < (3, 10):
    raise RuntimeError("Se requiere Python 3.10 o superior")

TOKENIZADOR = RegexpTokenizer(r"\w+")
STEMMER = SnowballStemmer("spanish")

# La prioridad impide que un saludo o palabra genérica oculte una solicitud específica.
# Todos los servicios descritos son EJEMPLOS, no un inventario real.
INTENCIONES = {
    "saludo": {
        "prioridad": 5,
        "patrones": ["hola", "buenos dias", "buenas tardes", "buenas noches", "que tal"],
        "respuesta": "¡Hola! Soy ConstructIA. Puedo orientarte sobre construcción y renta de maquinaria. ¿Qué necesitas?",
    },
    "solicitar_obra": {
        "prioridad": 90,
        "patrones": ["quiero construir", "necesito construir", "quiero remodelar", "necesito remodelar", "quiero ampliar", "necesito una ampliacion"],
        "respuesta": "Con gusto te ayudaré a preparar una solicitud de obra.",
    },
    "cotizacion": {
        "prioridad": 100,
        "patrones": ["cotizacion", "cotizar", "presupuesto", "cuanto cuesta", "precio", "tarifa", "costo"],
        "respuesta": "Puedo orientar tu solicitud. Un asesor debe confirmar el precio según equipo, obra, fecha, ubicación y condiciones; esta demo no consulta tarifas reales.",
    },
    "requisitos": {
        "prioridad": 75,
        "patrones": ["requisitos", "documentos", "que necesito para rentar", "condiciones de renta"],
        "respuesta": "Los documentos, depósito y condiciones dependen de cada proveedor. Un asesor deberá confirmarlos antes de contratar.",
    },
    "disponibilidad": {
        "prioridad": 80,
        "patrones": ["disponibilidad", "disponible", "tienen libre", "tienen para manana"],
        "respuesta": "La disponibilidad de equipos se debe verificar con el proveedor. Esta versión no consulta inventarios en tiempo real.",
    },
    "operador": {
        "prioridad": 77,
        "patrones": ["operador", "operadores", "maquinista", "incluye chofer"],
        "respuesta": "Puede solicitarse maquinaria con operador o sin él, sujeto a condiciones del proveedor y a las normas de seguridad aplicables.",
    },
    "contacto": {
        "prioridad": 65,
        "patrones": ["asesor", "contacto", "telefono", "whatsapp", "hablar con alguien"],
        "respuesta": "Esta demo recopila información en pantalla, pero todavía no envía mensajes a asesores ni almacena contactos.",
    },
    "renta_retroexcavadora": {
        "prioridad": 89,
        "patrones": ["retroexcavadora", "retroexcavadoras"],
        "respuesta": "Vamos a iniciar una solicitud de retroexcavadora.",
    },
    "renta_plataforma": {
        "prioridad": 89,
        "patrones": ["plataforma elevadora", "plataformas elevadoras", "plataforma", "plataformas", "elevador de tijera"],
        "respuesta": "Vamos a iniciar una solicitud de plataforma elevadora.",
    },
    "renta_minicargador": {
        "prioridad": 89,
        "patrones": ["minicargador", "minicargadores", "bobcat"],
        "respuesta": "Vamos a iniciar una solicitud de minicargador.",
    },
    "catalogo_maquinaria": {
        "prioridad": 40,
        "patrones": ["maquinaria", "maquinas", "equipos que rentan", "catalogo", "que equipos tienen"],
        "respuesta": "Catálogo ilustrativo: retroexcavadoras, plataformas elevadoras y minicargadores. Debe verificarse el inventario real de cada empresa.",
    },
    "servicios_construccion": {
        "prioridad": 35,
        "patrones": ["servicios de construccion", "construccion", "remodelaciones", "ampliaciones", "obras"],
        "respuesta": "El asistente puede registrar solicitudes de construcción, remodelación y ampliación; un especialista deberá evaluar cada obra.",
    },
    "zonas": {
        "prioridad": 60,
        "patrones": ["zona de servicio", "donde trabajan", "que municipios", "cobertura"],
        "respuesta": "Las zonas de servicio dependen de cada proveedor. Indica el municipio para anexarlo a una solicitud.",
    },
    "agradecimiento": {
        "prioridad": 10,
        "patrones": ["gracias", "muchas gracias"],
        "respuesta": "¡Con gusto! ¿Necesitas algo más?",
    },
    "despedida": {
        "prioridad": 12,
        "patrones": ["adios", "hasta luego", "nos vemos", "bye"],
        "respuesta": "¡Hasta luego! Gracias por utilizar ConstructIA.",
    },
}

EQUIPOS = {
    "renta_retroexcavadora": "retroexcavadora",
    "renta_plataforma": "plataforma elevadora",
    "renta_minicargador": "minicargador",
}


def normalizar(texto: str) -> str:
    """Minúsculas, espacios exteriores y acentos; conserva números."""
    texto = texto.strip().lower()
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def tokens(texto: str) -> list[str]:
    return TOKENIZADOR.tokenize(normalizar(texto))


def raices(texto: str) -> list[str]:
    return [STEMMER.stem(token) for token in tokens(texto)]


def patron_en(mensaje: list[str], patron: list[str]) -> bool:
    """Coincidencia por secuencias de raíces completas, no substrings."""
    n = len(patron)
    return bool(n) and any(mensaje[i:i + n] == patron for i in range(len(mensaje) - n + 1))


def identificar_intencion(mensaje: str) -> str:
    """Selecciona una sola intención según prioridad y longitud del patrón."""
    palabras = raices(mensaje)
    candidatos = []
    for nombre, datos in INTENCIONES.items():
        longitudes = [len(raices(p)) for p in datos["patrones"] if patron_en(palabras, raices(p))]
        if longitudes:
            candidatos.append((datos["prioridad"], max(longitudes), nombre))
    return max(candidatos)[2] if candidatos else "desconocida"


