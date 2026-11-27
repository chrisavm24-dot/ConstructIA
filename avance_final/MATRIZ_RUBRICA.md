# Matriz de cumplimiento del proyecto final - MBIA2602

| Criterio | Puntaje | Evidencia solicitada | Estado al crear esta matriz |
|---|---:|---|---|
| Web Streamlit + Flask | 25 | UI con entradas/resultados + manejo de errores | Código subido; pruebas integradas pendientes |
| NLP + visión + agente | 25 | Diagrama, funciones e intercambio de información y demostración | Agente y servicios escritos; visión requiere pesos ResNet50 |
| Nube/URL | 20 | URL pública funcional y evidencias de despliegue | Pendiente |
| Validación y análisis | 15 | Pruebas de la app + desempeño, escalabilidad, mantenibilidad, ética | Pruebas unitarias creadas; faltan ejecución integral y análisis con evidencia |
| Documento y presentación | 15 | Documento 15-20 cuartillas, GitHub, video 5-10 min, URL, diagrama, evidencias, métricas y plan futuro | GitHub y diagrama preparados; documento, video, URL y pruebas de nube pendientes |

## Pruebas funcionales propuestas

1. /health reporta estado del servicio y disponibilidad visual.
2. Consulta sin texto devuelve error controlado.
3. Consulta de precios: la intención final es cotización aunque SVM clasifique otra.
4. Solicitud de retroexcavadora: no se confunde con excavadora hidráulica.
5. Municipio proporcionado: se detecta sin inventar cobertura.
6. Solicitud con/sin operador: se respetan negaciones y preguntas.
7. Consulta de imagen sin pesos: error explícito 503.
8. Con pesos: fotografía válida de cada familia -> categoría y respuesta integrada.
9. Contradicción entre texto y fotografía -> advertencia y revisión humana.
10. Fotografía corrupta o >8MB -> manejo de error.
11. Restablecimiento y continuidad de estado conversacional.
12. URL pública en navegador ajeno; medir latencia y anotar fallos reales.
13. Uso repetido y límites de consumo de memoria; evitar persistir datos personales.
14. Grabar demo funcional 5-10 minutos y adjuntar enlace.

## Métricas iniciales, no nuevas

NLP: accuracy 0.644, F1 macro 0.631 con 45 ejemplos sintéticos reservados.
ResNet50: accuracy 0.720, F1 macro 0.698 con 25 fotografías de V3.

No presentar estas cifras como evaluación de V4: la aplicación final necesita sus propias pruebas técnicas y evidencia visual.
