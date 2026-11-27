# ConstructIA V4 - Proyecto final en desarrollo

Prototipo academico de atencion inicial para construccion y renta de maquinaria. No confirma tarifas, disponibilidad, reservas, marcas exactas ni idoneidad tecnica.

## Arquitectura

Usuario -> Streamlit -> API Flask -> agente hibrido -> respuesta Streamlit.

El agente combina el clasificador NLP SVM de avance2, el modelo visual ResNet50 (cuando existan pesos), la logica comercial de motor_solicitudes y el chatbot del Avance 1 con estado de conversacion. La respuesta identifica por separado la prediccion estadistica, las reglas aplicadas y la clase visual cuando esta disponible.

## Estado real

- Archivos web, API y agente creados; pendientes pruebas completas de extremo a extremo.
- NLP SVM disponible al entrenarse desde el dataset de avance2 (180 textos sinteticos); accuracy anterior 64.4%, no es una prueba nueva de V4.
- Vision ResNet50: **sin pesos entrenados** actualmente. La aplicacion no fabrica una clase visual; devuelve error 503 si se envia una imagen sin checkpoint.
- Despliegue y URL publica todavia pendientes, al igual que video y documento de 15-20 paginas.

## Pruebas

Desde la raiz del repositorio:

    python -m pip install "nltk>=3.8,<4"
    python -m unittest discover -s avance_final -p "test_*.py" -v

Las pruebas del agente sustituyen las predicciones de modelos por respuestas fijas: no validan accuracy ni precision de ResNet50 o SVM. Revisar los resultados reales en GitHub Actions.

## Flask (terminal 1)

    python -m pip install -r avance_final/requirements_api.txt
    python -m avance_final.api_flask

Salud de la API: http://127.0.0.1:5000/health

Ejemplo de texto: POST /api/interactuar con JSON que contenga texto y estado, por ejemplo {"texto":"Quiero cotizar una retroexcavadora en Monterrey","estado":{}}.

## Streamlit (terminal 2)

    python -m pip install -r avance_final/requirements_web.txt
    streamlit run avance_final/streamlit_app.py

La barra lateral permite escribir la URL http://127.0.0.1:5000. En Streamlit Community Cloud, usar la entrada avance_final/streamlit_app.py, rama main, y configurar la variable CONSTRUCTIA_API_URL en Secrets.

## Modelo visual

Es necesario volver a entrenar y guardar el checkpoint compatible con claves state_dict y clases, tal como generaba el notebook de ResNet50. Colocarlo fuera de GitHub en un servicio de almacenamiento persistente y configurarlo como archivo local mediante CONSTRUCTIA_MODEL_PATH. De forma predeterminada se busca en avance_final/modelos/constructia_resnet50.pt.

**Importante:** como el test de V3 ya fue revisado, una comparacion nueva necesita fotografias externas independientes. El sistema no debe presentar resultados antiguos como nuevas evaluaciones.

## Despliegue del backend

Opcion persistente: servicio Python Flask (por ejemplo Render), comando de instalacion:

    pip install -r avance_final/requirements_api.txt

Comando de inicio:

    gunicorn avance_final.api_flask:app --bind 0.0.0.0:$PORT

Comprobar limites de RAM de PyTorch y disponibilidad de los pesos. No se ha desplegado todavia.

Opcion para demostracion temporal: Cloudflare Quick Tunnel con Flask local activo:

    cloudflared tunnel --url http://127.0.0.1:5000

La URL trycloudflare.com es efimera: no sustituye un servicio publico persistente y deja de funcionar al detener el tunel.

## Errores y etica

Limites a entradas, archivos 8MB, reporte explicito de modelo faltante, registro de tiempo/codigo HTTP/ID sin contenido de conversaciones. El chat mantiene el estado en el cliente; no guarda imagenes ni datos en base de datos. No publicar datos reales de clientes sin autorizacion, seguridad y politica de privacidad. Siempre debe existir validacion humana de precio, ubicacion, disponibilidad y aspectos de seguridad.

## Entrega exigida

Rubrica final: web con Streamlit y Flask (25), integracion de chatbot NLP, vision y agente (25), despliegue funcional con URL publica y capturas (20), pruebas y analisis de desempeño, escalabilidad, mantenibilidad y etica (15), documentacion (15). Documentacion: 15-20 cuartillas; video demo: 5-10 minutos; URL, GitHub, arquitectura, pruebas, metricas y mejoras futuras.

Proximo hito: verificar pruebas de API y app, recuperar los pesos ResNet50, desplegar, capturar evidencia y terminar el reporte.
