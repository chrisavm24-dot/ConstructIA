from constructia_reglas import INTENCIONES, EQUIPOS, normalizar, identificar_intencion

class ConstructIA:
    """Estado temporal de un único chat; no almacena datos después de la sesión."""

    def __init__(self):
        self.paso: str | None = None
        self.datos: dict[str, str] = {}
        self.ultima_intencion: str | None = None

    def iniciar_solicitud(self, tipo: str, equipo: str | None = None) -> str:
        self.datos = {"servicio": tipo}
        if equipo:
            self.datos["equipo"] = equipo
        self.paso = "tipo_obra" if tipo == "construccion" else "ubicacion"
        if tipo == "construccion":
            return "Solicitud de construcción: ¿qué deseas construir o remodelar?"
        return f"Solicitud de {equipo}: ¿en qué municipio se utilizará el equipo?"

    def guardar_dato(self, mensaje: str) -> str:
        valor = mensaje.strip()
        if len(valor) < 2:
            return "Necesito más información. Escribe nuevamente tu respuesta, por favor."
        if self.paso == "tipo_obra":
            self.datos["tipo_obra"] = valor
            self.paso = "ubicacion"
            return "¿En qué municipio se realizaría la obra?"
        if self.paso == "ubicacion":
            self.datos["municipio"] = valor
            self.paso = "medidas" if self.datos["servicio"] == "construccion" else "fecha"
            return "¿Qué medidas aproximadas tendrá la obra?" if self.paso == "medidas" else "¿Para qué fecha necesitas la maquinaria?"
        if self.paso == "medidas":
            self.datos["medidas_aproximadas"] = valor
            self.paso = "fecha"
            return "¿Cuándo te gustaría comenzar la obra?"
        if self.paso == "fecha":
            self.datos["fecha_solicitada"] = valor
            self.paso = "duracion" if self.datos["servicio"] == "renta_maquinaria" else "contacto"
            return "¿Por cuántos días u horas requieres la maquinaria?" if self.paso == "duracion" else "Escribe nombre y contacto ficticios para la demostración."
        if self.paso == "duracion":
            self.datos["duracion"] = valor
            self.paso = "operador"
            return "¿La necesitas con operador o sin operador?"
        if self.paso == "operador":
            self.datos["operador"] = valor
            self.paso = "contacto"
            return "Escribe nombre y contacto ficticios para la demostración."
        if self.paso == "contacto":
            self.datos["contacto_demo"] = valor
            self.paso = None
            resumen = " | ".join(f"{campo}: {dato}" for campo, dato in self.datos.items())
            return "SOLICITUD DEMO (solo en memoria): " + resumen + ". No se ha enviado ni reservado nada."
        return "No pude continuar. Escribe 'cancelar' para reiniciar."

    def responder(self, mensaje: str) -> str:
        normal = normalizar(mensaje)
        if normal in {"cancelar", "cancelar solicitud", "reiniciar"}:
            self.paso, self.datos = None, {}
            self.ultima_intencion = "cancelacion"
            return "Solicitud cancelada. ¿Necesitas construcción o renta de maquinaria?"
        if normal == "salir":
            self.paso, self.datos = None, {}
            self.ultima_intencion = "despedida"
            return "¡Hasta luego! Gracias por utilizar ConstructIA."
        if not normal:
            self.ultima_intencion = "entrada_vacia"
            return "Escribe tu consulta para continuar."
        if self.paso is not None:
            self.ultima_intencion = "dato_" + self.paso
            return self.guardar_dato(mensaje)
        intencion = identificar_intencion(mensaje)
        self.ultima_intencion = intencion
        if intencion == "solicitar_obra":
            return self.iniciar_solicitud("construccion")
        if intencion in EQUIPOS:
            return self.iniciar_solicitud("renta_maquinaria", EQUIPOS[intencion])
        return INTENCIONES[intencion]["respuesta"] if intencion in INTENCIONES else (
            "No identifiqué tu consulta. Puedo orientar sobre construcción, maquinaria, requisitos y cotizaciones."
        )


