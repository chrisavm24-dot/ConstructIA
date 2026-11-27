"""Inferencia NLP y visión. No genera predicciones visuales sin pesos entrenados."""
from __future__ import annotations
from functools import lru_cache
from io import BytesIO
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = ROOT / "avance_final" / "modelos" / "constructia_resnet50.pt"
CLASES = ("retroexcavadora", "plataforma_elevadora", "minicargador")


class ModeloNoDisponible(RuntimeError):
    pass


@lru_cache(maxsize=1)
def cargar_nlp():
    from avance2.nlp_modelo import entrenar_y_evaluar
    return entrenar_y_evaluar()["pipeline"]


def clasificar_texto(texto: str) -> str:
    from avance2.nlp_modelo import predecir
    return predecir(cargar_nlp(), texto)["intencion_predicha"]


def ruta_modelo() -> Path:
    return Path(os.environ.get("CONSTRUCTIA_MODEL_PATH", str(DEFAULT_MODEL)))


def vision_disponible() -> bool:
    return ruta_modelo().is_file()


@lru_cache(maxsize=1)
def cargar_vision():
    ruta = ruta_modelo()
    if not ruta.is_file():
        raise ModeloNoDisponible(
            "Falta el archivo de pesos ResNet50. "
            "Debes recuperarlo o volver a entrenar y respaldar el modelo."
        )
    import torch
    from torch import nn
    from torchvision import models, transforms
    # Solo debe cargarse un checkpoint creado por nuestro propio cuaderno.
    checkpoint = torch.load(ruta, map_location="cpu", weights_only=True)
    clases = checkpoint.get("clases")
    if not isinstance(clases, (list, tuple)) or set(clases) != set(CLASES):
        raise ModeloNoDisponible("El checkpoint no contiene las tres clases esperadas.")
    red = models.resnet50(weights=None)
    red.fc = nn.Linear(red.fc.in_features, len(clases))
    red.load_state_dict(checkpoint["state_dict"], strict=True)
    red.eval()
    procesado = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    return red, procesado, list(clases)


def clasificar_imagen(contenido: bytes) -> str:
    if not contenido:
        raise ValueError("No se recibió una imagen.")
    if len(contenido) > 8 * 1024 * 1024:
        raise ValueError("La imagen excede el límite de 8 MB.")
    from PIL import Image, ImageOps, UnidentifiedImageError
    try:
        imagen = Image.open(BytesIO(contenido))
        if imagen.format not in {"JPEG", "PNG", "WEBP"}:
            raise ValueError("Solo se permiten imágenes JPEG, PNG o WEBP.")
        imagen = ImageOps.exif_transpose(imagen).convert("RGB")
        if imagen.width * imagen.height > 25_000_000:
            raise ValueError("La resolución de la imagen es demasiado grande.")
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("No se pudo interpretar el archivo como imagen.") from exc
    red, procesado, clases = cargar_vision()
    import torch
    with torch.no_grad():
        salida = red(procesado(imagen).unsqueeze(0))
        indice = int(salida.argmax(dim=1).item())
    return clases[indice]
