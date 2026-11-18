# ConstructIA — Avance 2: resultados preliminares verificables

> Documento de trabajo para redactar el reporte académico. Los valores siguientes se transcriben de las **capturas reales de Google Colab de la versión V3 original**, aportadas por el estudiante. No son resultados obtenidos con V3.1 y no equivalen a métricas de producción.

## 1. Recuperación del Avance 1

Se conserva la problemática de atención inicial de solicitudes de construcción y renta de maquinaria, los usuarios objetivo y 15 intenciones conversacionales. V2 implementó detección basada en reglas; en el Avance 2 se agrega un clasificador NLP entrenado y una CNN de imágenes.

## 2. Componente textual

- Dataset creado para la práctica: 180 mensajes **sintéticos**, 15 intenciones, 12 ejemplos por clase.
- Normalización, tokenización, eliminación de stopwords y stemming español. Se conservan negaciones («no», «sin») por su relevancia para las solicitudes.
- Representación: TF-IDF. División estratificada 135 entrenamiento / 45 prueba; selección del modelo por validación cruzada en entrenamiento.
- F1 macro medio de validación cruzada: Naive Bayes 0.496; SVM lineal 0.537.
- Modelo elegido: SVM lineal.
- Evaluación de prueba: accuracy **0.644**; precisión macro **0.723**; recall macro **0.644**; F1 macro **0.631**.
- Matriz de confusión: 29 de 45 predicciones correctas. La clase `disponibilidad` obtuvo 0 de 3 casos correctos; `renta_retroexcavadora`, `renta_plataforma` y `catalogo_maquinaria` obtuvieron 3 de 3. El tamaño del test por clase (n=3) exige cautela.
- Consulta adicional: «Quiero saber el precio de una plataforma elevadora» fue clasificada erróneamente como `renta_plataforma`. No se oculta el error.

**Interpretación:** el modelo se entrenó y evaluó adecuadamente, pero el pequeño vocabulario sintético y la ambigüedad entre intenciones reducen la generalización. La priorización comercial de V3.1 no cambia estas métricas del clasificador.

## 3. Componente visual (experimento original V3)

- Fotografías de Wikimedia Commons con fuente, autor y licencia registrados.
- 165 fotografías descargadas: 55 retroexcavadoras, 55 plataformas elevadoras y 55 minicargadores.
- Separación: 115 imágenes de entrenamiento, 25 de validación y 25 de prueba.
- Arquitectura: ResNet50 con pesos ImageNet, extractor convolucional congelado y nueva capa final de 3 clases.
- Cinco épocas; el mejor F1 macro de validación observado fue **0.843**.
- Evaluación reservada de V3: **accuracy 0.720**, **precisión macro 0.710**, **recall macro 0.708** y **F1 macro 0.698**.
- Aciertos por clase: retroexcavadora 5/8; plataforma elevadora 9/9; minicargador 4/8.

**Limitación observada:** la vista de revisión incluyó fotos poco representativas (una intersección, un panel de control y un camión que transporta maquinaria). La pertenencia a una categoría de Commons no garantiza que una foto sea adecuada para clasificación. La curación está implementada en V3.1, pero sus resultados deberán registrarse solo después de volver a ejecutar el cuaderno y revisar todas las etiquetas.

## 4. Integración inicial

En V3 se utilizó la consulta «Me gustaría conocer el precio para rentar una máquina» junto a una fotografía de prueba; el clasificador de texto predijo `catalogo_maquinaria`, mientras que ResNet50 predijo `retroexcavadora`. El sistema comunicó ambas predicciones. La intención comercial era de cotización: se detectó un error relevante de NLP.

En V3.1 se agregó una **regla explícita y auditable** que prioriza consultas que contienen «precio», «costo», «tarifa», «cotizar» o «presupuesto». La nueva salida mostrará tanto la predicción original SVM como la decisión comercial final. **Aún no hay evidencia de ejecución de esta modificación en Google Colab.**

## 5. Principales conclusiones y mejoras

1. Los modelos funcionan como demostración técnica multimodal, pero las métricas obtenidas en datasets reducidos no avalan su uso comercial.
2. Debe ampliarse el corpus textual con frases naturales, variaciones, consultas mixtas y mensajes fuera del alcance.
3. Se requiere curar las imágenes (incluidas múltiples perspectivas), controlar equipos/series duplicados entre particiones y ampliar el dataset con fuentes independientes.
4. Un asesor debe confirmar la cotización, la seguridad, la disponibilidad y la identificación exacta del equipo.
5. **Validación futura:** tras haber inspeccionado el test V3, la iteración V3.1 se considera exploratoria. Para verificar mejoras reales será necesario recopilar un nuevo test externo no utilizado en ninguna decisión de desarrollo.

## 6. Evidencias ya disponibles y pendientes

| Componente | Evidencia del estudiante | Estado |
|---|---|---|
| Corpus y preprocesamiento | Capturas de Colab: 180 mensajes, 4 técnicas | Registrada |
| NLP: entrenamiento/evaluación | Métricas y matriz de confusión sobre 45 mensajes | Registrada |
| CNN: dataset | Descarga de 165 imágenes y división 115/25/25 | Registrada, curación incompleta |
| CNN: evaluación | Historial de cinco épocas, reporte y matriz de confusión | Registrada (V3) |
| Integración texto–imagen | Respuesta conjunta con error de cotización visible | Registrada (V3) |
| V3.1: nueva curación y regla comercial | Nuevo cuaderno publicado en GitHub | **Falta ejecutar en Colab y documentar** |

Esta tabla mantiene separados el cumplimiento de actividades, los resultados experimentales y la validación que todavía falta.
