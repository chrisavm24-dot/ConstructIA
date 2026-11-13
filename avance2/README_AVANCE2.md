# ConstructIA — Avance de proyecto 2

**Origen:** continuación del chatbot de reglas del Avance 1.

## Fase textual terminada para evaluación en Colab

- `datos/intenciones_constructia.csv`: 180 mensajes ficticios para entrenamiento y pruebas (12 por cada una de las 15 intenciones originales).
- `nlp_modelo.py`: normalización, tokenización NLTK, eliminación de stopwords, stemming Snowball, TF-IDF, Naive Bayes y SVM. División estratificada 75/25, selección por validación cruzada solo en entrenamiento, evaluación reservada.
- `ConstructIA_Avance2_NLP_Colab.ipynb`: guía paso a paso con tablas, métricas, matriz de confusión y discusión.

## Resultados de referencia local

Modelo elegido por F1 macro de validación cruzada: **SVM lineal** (vs. Naive Bayes). En la partición de prueba de 45 ejemplos sintéticos, accuracy = **0.644**, precision macro = **0.723**, recall macro = **0.644** y F1 macro = **0.631**.

Estos resultados se obtuvieron en Python local con el dataset ficticio; se deben volver a verificar en Colab. **No son medidas de precisión en clientes reales.**

## Próxima fase visual

Tres clases previstas: retroexcavadora, plataforma elevadora y minicargador. Se requiere un dataset con imágenes que tengamos derecho de utilizar, con variedad de ángulos, fondos e iluminación, y separación de imágenes originales por entrenamiento/validación/prueba para evitar fuga de datos. Se entrenará ResNet50 con transfer learning y cinco evidencias: accuracy, precision, recall, F1 y matriz de confusión.

## Integración multimodal prevista

Consulta de texto → PLN clasifica la intención; foto opcional → CNN sugiere categoría de equipo; el asistente combina ambas salidas y solicita ubicación/fecha/duración, pero no confirma una reserva ni prescribe equipos para una obra.
