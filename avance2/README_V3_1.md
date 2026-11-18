# ConstructIA V3.1 — curación y prioridad comercial

Esta carpeta conserva el cuaderno original `ConstructIA_Avance2_ResNet50_Colab.ipynb` **sin alterarlo**. La iteración nueva está en `ConstructIA_Avance2_V3_1_Colab.ipynb`.

## Cambios implementados

1. **Fotografías:** mantiene el registro completo de autor, licencia y página original. Marca para exclusión preliminar tres títulos vistos en capturas de V3 (intersección lejana, panel de control y camión de transporte), si vuelven a aparecer. Muestra los títulos coincidentes, guarda un CSV de exclusiones y genera páginas de 20 fotos para revisión total. Permite añadir **IDs de revisión** y evita entrenar hasta que la auditoría humana se confirme.
2. **Respuesta comercial:** el archivo `integracion_prioridades.py` conserva la clase original predicha por SVM y aplica una regla trazable para preguntas explícitas de **precio/costo/tarifa/cotización**; así la respuesta integrada prioriza `cotizacion` sin inventar una tarifa.
3. **Respaldo:** celda opcional para copiar modelos y manifiestos a Google Drive después del entrenamiento.

## Abrir V3.1

https://colab.research.google.com/github/chrisavm24-dot/ConstructIA/blob/main/avance2/ConstructIA_Avance2_V3_1_Colab.ipynb

**Orden:** iniciar entorno → descargar fotografías → correr revisión de títulos → revisar las galerías de toda la colección → añadir IDs incorrectos si los hubiera → cambiar `AUDITORIA_VISUAL_CONFIRMADA = True` **solo cuando corresponda** → separar conjuntos → entrenar ResNet50 → evaluar → ejecutar integración → respaldar.

## Resultados que sí tenemos (V3 original)

Los siguientes valores **son del cuaderno V3 original, no de V3.1**:

| Módulo | Prueba reservada | Accuracy | F1 macro |
|---|---:|---:|---:|
| Texto: SVM + TF-IDF | 45 mensajes sintéticos | 0.644 | 0.631 |
| Visión: ResNet50 | 25 fotos | 0.720 | 0.698 |

La evaluación visual fue 5/8 retroexcavadoras, 9/9 plataformas elevadoras y 4/8 minicargadores. La muestra es pequeña y las etiquetas del dataset requieren curación.

**Advertencia:** ya se inspeccionó la prueba de V3. Cualquier nueva evaluación de V3.1 usando estas mismas fotografías o una nueva partición de ellas es **exploratoria**, no equivale a un test independiente y no debe reportarse como una mejora de precisión en producción. Para determinar capacidad de generalización, reunir fotografías externas nuevas y revisar las licencias, duplicados y etiquetado antes de usarlas.

## Límites

- El código puede **señalar** fotos claramente cuestionables por sus títulos, pero no puede certificar la clase de todas las imágenes sin revisión visual.
- La regla comercial no reentrena SVM ni corrige sus errores estadísticos; actúa después de su predicción y se reporta por separado.
- Las clasificaciones no aseguran modelo exacto, disponibilidad, idoneidad técnica o seguridad de la maquinaria.
