"""ConstructIA Avance 2: clasificación de intenciones (datos didácticos).

Requiere Python >=3.10, nltk, pandas, scikit-learn y matplotlib (solo gráficos).
Conserva el chatbot de reglas del Avance 1; este módulo construye el clasificador ML.
"""
from __future__ import annotations
import re
import unicodedata
from pathlib import Path

import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

RUTA_DATOS = Path(__file__).resolve().parent / 'datos' / 'intenciones_constructia.csv'
TOKENIZADOR = RegexpTokenizer(r'[a-z0-9]+')
STEMMER = SnowballStemmer('spanish')
NEGACIONES = {'no', 'nunca', 'sin', 'ni', 'tampoco'}
# Lista fija y auditable de palabras frecuentes en español: evita descargas y
# mantiene idéntico procesamiento en Colab y en Python local.
STOPWORDS_ES = set("""a al algo algunas algunos ante antes como con contra cual cuales cuando
   de del desde donde durante e el ella ellas ellos en entre era eran eres es esa esas ese esos
   esta estaba estaban estamos estan estar estas este esto estos fue fueron ha habia han hasta
   hay la las le les lo los mas me mi mis mucho muy nada nos nosotras nosotros nuestra nuestras
   nuestro nuestros o os otra otras otro otros para pero por porque que quien quienes se sea sean
   ser si sido siendo sobre su sus tambien te tiene tienen todo todos tu tus un una unas uno unos
   usted ustedes ya yo""".split()) - NEGACIONES


def obtener_stopwords() -> set[str]:
    return STOPWORDS_ES.copy()


def normalizar(texto: str) -> str:
    texto = str(texto).strip().lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'\s+', ' ', texto)
    return texto


def procesar_texto(texto: str, palabras_vacias: set[str] | None = None) -> dict:
    """Ejecuta 4 pasos: normalización, tokenización, stopwords, stemming.

    Conservamos negaciones, porque 'con operador' y 'sin operador' no son equivalentes.
    """
    if palabras_vacias is None:
        palabras_vacias = obtener_stopwords()
    normalizado = normalizar(texto)
    tokens = TOKENIZADOR.tokenize(normalizado)
    filtrados = [x for x in tokens if x not in palabras_vacias]
    raices = [STEMMER.stem(x) for x in filtrados]
    return {'original': texto, 'normalizado': normalizado, 'tokens': tokens,
            'sin_stopwords': filtrados, 'stemming': raices, 'texto_procesado': ' '.join(raices)}


def cargar_datos(ruta=RUTA_DATOS):
    df = pd.read_csv(ruta)
    esperadas = {'texto', 'intencion', 'origen'}
    if not esperadas.issubset(df.columns):
        raise ValueError(f'Faltan columnas: {esperadas - set(df.columns)}')
    if df[['texto', 'intencion']].isna().any().any():
        raise ValueError('Hay mensajes o etiquetas vacíos')
    if df['texto'].duplicated().any():
        raise ValueError('Hay mensajes duplicados que podrían contaminar la evaluación')
    df['normalizado'] = df['texto'].map(normalizar)
    if df['normalizado'].duplicated().any():
        raise ValueError('Hay mensajes equivalentes después de normalizar')
    return df


def entrenar_y_evaluar(ruta=RUTA_DATOS):
    df = cargar_datos(ruta)
    vacias = obtener_stopwords()
    df['procesado'] = df['texto'].map(lambda t: procesar_texto(t, vacias)['texto_procesado'])
    # Estratificación: cada intención aparece en entrenamiento y prueba.
    X_ent, X_pr, y_ent, y_pr = train_test_split(df['procesado'], df['intencion'],
                             test_size=0.25, random_state=42, stratify=df['intencion'])
    # Comparamos Naive Bayes y SVM solo usando los 135 ejemplos de entrenamiento.
    # Esta validación cruzada evita elegir el modelo por su desempeño en el test final.
    candidatos = {
        'Naive Bayes': MultinomialNB(alpha=0.5),
        'SVM lineal': LinearSVC(C=1.0, random_state=42),
    }
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
    comparacion = {}
    for nombre, clasificador in candidatos.items():
        candidato = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), lowercase=False)),
            ('clasificador', clasificador),
        ])
        puntajes = cross_val_score(candidato, X_ent, y_ent, cv=cv, scoring='f1_macro')
        comparacion[nombre] = float(puntajes.mean())
    elegido = max(comparacion, key=comparacion.get)
    # TF-IDF se ajusta SOLO con entrenamiento; evitamos fuga desde el test.
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), lowercase=False)),
        ('clasificador', candidatos[elegido]),
    ])
    pipeline.fit(X_ent, y_ent)
    y_pred = pipeline.predict(X_pr)
    prec, rec, f1, _ = precision_recall_fscore_support(y_pr, y_pred, average='macro', zero_division=0)
    metricas = {'accuracy': float(accuracy_score(y_pr, y_pred)),
                'precision_macro': float(prec), 'recall_macro': float(rec), 'f1_macro': float(f1),
                'num_entrenamiento': len(X_ent), 'num_prueba': len(X_pr), 'clases': df['intencion'].nunique(),
                'vocabulario_tfidf': len(pipeline.named_steps['tfidf'].vocabulary_),
                'modelo_elegido': elegido, 'f1_cv_entrenamiento': comparacion}
    detalles = pd.DataFrame({'consulta_original': df.loc[X_pr.index, 'texto'].values,
                             'intencion_real': y_pr.values, 'intencion_predicha': y_pred})
    detalles['correcto'] = detalles['intencion_real'] == detalles['intencion_predicha']
    etiquetas = sorted(df['intencion'].unique())
    matriz = confusion_matrix(y_pr, y_pred, labels=etiquetas)
    reporte = classification_report(y_pr, y_pred, labels=etiquetas, zero_division=0)
    return {'datos': df, 'pipeline': pipeline, 'metricas': metricas, 'detalles': detalles,
            'matriz': matriz, 'etiquetas': etiquetas, 'reporte': reporte}


def predecir(modelo, mensaje: str):
    procesado = procesar_texto(mensaje)['texto_procesado']
    prediccion = str(modelo.predict([procesado])[0])
    # LinearSVC no produce probabilidades calibradas; no mostramos confianza engañosa.
    return {'mensaje': mensaje, 'texto_procesado': procesado, 'intencion_predicha': prediccion}


if __name__ == '__main__':
    r = entrenar_y_evaluar()
    print('Dataset:', len(r['datos']), 'ejemplos de', r['metricas']['clases'], 'intenciones')
    print('Métricas con prueba estratificada no vista:', r['metricas'])
    print(r['reporte'])
    print('Errores:', r['detalles'].loc[~r['detalles']['correcto']].to_string(index=False))
