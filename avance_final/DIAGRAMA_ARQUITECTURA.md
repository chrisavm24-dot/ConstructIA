# Diagrama de arquitectura - ConstructIA V4 (propuesta implementada)

El siguiente diagrama distingue **flujo y responsabilidades**. Los resultados de V3 solo sirven como antecedentes, no certifican el comportamiento de V4 desplegado.

~~~mermaid
flowchart TD
    U[Usuario] -->|Consulta y foto opcional| UI[Interfaz Streamlit]
    UI -->|POST /api/interactuar| API[API REST Flask]
    API --> AG[Agente híbrido / coordinador]
    AG --> NLP[SVM + TF-IDF\n15 intenciones]
    AG --> CHAT[Chatbot V2\nflujo con estado]
    AG --> RULES[Reglas comerciales\ncotización y campos]
    AG --> VIS{¿Hay fotografía?}
    VIS -->|Sí| CNN[ResNet50 entrenada\nrequiere checkpoint .pt]
    VIS -->|No| AG
    CNN -->|Categoría de maquinaria| AG
    NLP -->|Intención detectada| AG
    CHAT -->|Respuesta y estado| AG
    RULES -->|Ajuste y alertas| AG
    AG -->|Respuesta + advertencias| API
    API -->|JSON / errores HTTP| UI
    UI --> U
~~~

**Límites verificables:**
- Sin el checkpoint ResNet50 el backend debe contestar HTTP 503 en una solicitud con imagen, no fingir una clasificación.
- La detección de una categoría no confirma máquina exacta, existencias, precios, permisos o seguridad.
- La API no persiste mensajes; el estado vuelve al cliente y solo vive en su sesión.
- La URL pública, las pruebas externas y la curación visual siguen pendientes.

**Intercambio de datos clave:**
- Streamlit -> Flask: texto de usuario, estado conversacional y binario opcional de imagen.
- Flask -> SVM: texto preprocesado -> intención original.
- Flask -> ResNet50: fotografía -> categoría sugerida.
- Agente: combina intención, reglas comerciales y respuesta del chatbot; detecta discrepancias y consulta faltante.
- Flask -> Streamlit: respuesta, intención ML, intención final, categoría visual, estado y advertencia.
