"""Interfaz web ConstructIA. Necesita API REST en URL configurable."""
from __future__ import annotations
import os
import requests
import streamlit as st

st.set_page_config(page_title="ConstructIA", page_icon="🏗️", layout="centered")
st.title("🏗️ ConstructIA")
st.caption("Asistente académico de construcción y renta de maquinaria · prototipo")
st.info("Las tarifas, la disponibilidad y las características técnicas requieren confirmación humana.")

if "conversaciones" not in st.session_state:
    st.session_state.conversaciones = []
if "estado" not in st.session_state:
    st.session_state.estado = {}

with st.sidebar:
    st.header("Configuración")
    valor_inicial = os.environ.get("CONSTRUCTIA_API_URL", "")
    try:
        valor_inicial = st.secrets.get("CONSTRUCTIA_API_URL", valor_inicial)
    except Exception:
        pass
    url = st.text_input("URL de la API Flask", value=valor_inicial,
                        help="Ejemplo: https://tu-api.example.com (sin barra final)")
    if st.button("Reiniciar conversación"):
        st.session_state.conversaciones = []
        st.session_state.estado = {}
        st.rerun()
    if url:
        try:
            r = requests.get(url.rstrip("/") + "/health", timeout=8)
            r.raise_for_status()
            estado = r.json()
            st.success("API conectada")
            if estado.get("vision") != "disponible":
                st.warning("La visión no tiene pesos entrenados cargados.")
        except requests.RequestException:
            st.error("No se puede contactar la API Flask.")
    else:
        st.warning("Configura una API Flask para utilizar el asistente.")

for item in st.session_state.conversaciones:
    with st.chat_message("user"):
        st.write(item["consulta"])
        if item.get("imagen"):
            st.caption("Se adjuntó una fotografía.")
    with st.chat_message("assistant"):
        st.write(item["respuesta"])
        if item.get("detalle"):
            with st.expander("Ver interpretación técnica"):
                st.json(item["detalle"])

with st.form("consulta_constructia", clear_on_submit=True):
    consulta = st.text_area("Escribe tu consulta", placeholder="Quiero cotizar una retroexcavadora en Monterrey")
    imagen = st.file_uploader("Fotografía opcional (JPG, PNG o WEBP)", type=["jpg", "jpeg", "png", "webp"])
    enviar = st.form_submit_button("Enviar solicitud", use_container_width=True)

if enviar:
    if not url:
        st.error("Antes de enviar, escribe la URL de la API Flask en la barra lateral.")
    elif not consulta.strip():
        st.error("Escribe una consulta.")
    else:
        try:
            archivos = None
            if imagen is not None:
                if imagen.size > 8 * 1024 * 1024:
                    st.error("La imagen supera 8 MB.")
                    st.stop()
                archivos = {"imagen": (imagen.name, imagen.getvalue(), imagen.type)}
            import json
            datos = {"texto": consulta, "estado": json.dumps(st.session_state.estado)}
            with st.spinner("Analizando consulta..."):
                res = requests.post(url.rstrip("/") + "/api/interactuar",
                                    data=datos, files=archivos, timeout=90)
            payload = res.json()
            if res.status_code != 200:
                st.error(payload.get("error", "No se pudo completar la consulta."))
            else:
                st.session_state.estado = payload.get("estado", {})
                st.session_state.conversaciones.append({
                    "consulta": consulta,
                    "imagen": imagen is not None,
                    "respuesta": payload["respuesta"],
                    "detalle": {
                        "intencion_svm": payload.get("intencion_svm"),
                        "intencion_final": payload.get("intencion_final"),
                        "clase_visual": payload.get("clase_visual"),
                        "regla_aplicada": payload.get("regla_aplicada"),
                    },
                })
                st.rerun()
        except (requests.RequestException, ValueError):
            st.error("No se pudo conectar con la API o procesar su respuesta.")
