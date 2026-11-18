# ConstructIA V3 — Visión con datos públicos

Continuación del Avance 2 del proyecto académico de Tecmilenio.

## Origen de las imágenes

El cuaderno obtiene imágenes **desde Wikimedia Commons al ejecutarse**, con tres categorías:

- [Backhoe loaders](https://commons.wikimedia.org/wiki/Category:Backhoe_loaders) → `retroexcavadora`
- [Scissor lifts](https://commons.wikimedia.org/wiki/Category:Scissor_lifts) → `plataforma_elevadora`
- [Skid-steer loaders](https://commons.wikimedia.org/wiki/Category:Skid-steer_loaders) → `minicargador`

Algunas imágenes proceden de subcategorías específicas de fabricantes o equipos. El programa filtra licencias públicas reconocibles como CC BY, CC BY-SA, CC0 y dominio público, y genera `origen_licencias_imagenes.csv` con título, autor, URL y licencia de cada fotografía. Las imágenes **no se copian a GitHub**; cada archivo tiene condiciones de atribución que hay que respetar. Las etiquetas pueden tener errores, por lo que debe hacerse revisión visual humana.

## Uso

Abrir [ConstructIA_Avance2_ResNet50_Colab.ipynb](ConstructIA_Avance2_ResNet50_Colab.ipynb) en Google Colab y ejecutar las celdas en orden.

El cuaderno descarga una muestra inicial de hasta 55 fotografías por clase, intenta deduplicarlas, realiza partición estratificada, entrena **ResNet50** con transferencia de aprendizaje, calcula accuracy/precision/recall/F1-score y matriz de confusión, y enseña un ejemplo de integración con el clasificador NLP SVM del Avance 2.

**Importante:** el entrenamiento y sus métricas **no están precalculados**: se obtendrán cuando el usuario ejecute el cuaderno. El dataset generado no está curado en su totalidad y no es apto aún para producción ni para tomar decisiones de seguridad.
