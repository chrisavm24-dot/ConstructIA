# ConstructIA — preparación de la entrega final

Esta carpeta se creó **después** de los Avances 1 y 2. Se mantiene separada para no modificar los archivos ni las métricas ya entregadas. **No representa una aplicación comercial terminada.**

## Mejoras de base implementadas

- `motor_solicitudes.py`: añade una capa de lógica empresarial que recibe una intención previamente clasificada (por SVM u otro clasificador), detecta lenguaje de cotización, extrae municipio y equipo expresamente mencionados, identifica solicitudes claras sobre operador y señala discrepancias entre maquinaria escrita y sugerida por imagen.
- `test_motor_solicitudes.py`: pruebas unitarias para cotización, municipios, operador, casos ambiguos, diferencias entre texto/foto y prohibición de confirmar precios.

**No se modifica el modelo SVM, ResNet50 ni sus resultados originales.** Las métricas del Avance 2 siguen siendo 64.4% accuracy (NLP) y 72% accuracy (ResNet50), sobre los conjuntos de prueba académicos ya descritos.

## Cómo ejecutar pruebas en Python

Desde la raíz del repositorio:

```bash
python -m unittest discover -s avance_final -p "test_*.py" -v
```

Las pruebas nuevas usan solamente la biblioteca estándar de Python. Antes de integrar esta carpeta al cuaderno final conviene **ejecutarlas y conservar la salida real**; crear el archivo de pruebas no demuestra por sí mismo que ya pasaron.

Ejemplo de llamada para cuando exista un modelo cargado:

```python
from avance_final.motor_solicitudes import analizar_solicitud, responder_orientacion
resultado = analizar_solicitud(
    "Necesito el precio de una plataforma elevadora en Monterrey",
    intencion_svm="renta_plataforma",
    clase_visual="plataforma_elevadora",
)
print(resultado)
print(responder_orientacion(resultado))
```

## Qué falta antes de la entrega final

1. Leer la nueva **rúbrica e instrucciones** antes de decidir qué funcionalidad es obligatoria.
2. Validar las fotografías de cada clase con revisión humana; evitar etiquetas incorrectas y duplicados de un mismo equipo entre particiones.
3. Ejecutar el entrenamiento y los tests de la versión actualizada; no reutilizar métricas antiguas como si fueran resultados nuevos.
4. Validar fuera del pequeño dataset sintético: casos de desconocidos, preguntas mixtas y consultas no previstas; utilizar un conjunto de prueba externo nuevo.
5. Definir un canal seguro de recepción de solicitudes y consentimiento, política de almacenamiento y contacto con proveedores **si** la entrega final pide una aplicación web o un prototipo operativo.
6. Preparar la evidencia de ejecución, el documento académico y la explicación oral conforme a la rúbrica final.

## Limitaciones actuales

- Reconocer un municipio mencionado **no significa** confirmar cobertura del servicio.
- Una foto clasificada **no identifica** marca, modelo ni capacidad exacta.
- La detección de datos es parcial: no valida direcciones, fechas, duraciones o teléfonos; no recibe pagos ni genera reservas.
- Ante discrepancias entre el texto y la imagen se solicita revisión humana.
- Las reglas comerciales se reportan separadas de los resultados estadísticos del clasificador.

El desarrollo sigue siendo un prototipo académico y no está destinado a asesoramiento técnico sobre seguridad de maquinaria.
