
"""Define las entidades principales del sistema Software FJ."""

from abc import ABC, abstractmethod
from excepciones import ValidationError


class Entidad(ABC):
    """Clase abstracta base para las entidades del sistema."""

    def __init__(self, identificador):
        """Inicializa una entidad con un identificador obligatorio."""
        if not identificador:
            raise ValidationError("El identificador es obligatorio.")

        self._identificador = identificador

    @property
    def identificador(self):
        """Devuelve el identificador de la entidad."""
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        """Define el método que muestra la información de cada entidad."""
        pass


class Cliente(Entidad):
    """Representa a un cliente registrado en Software FJ."""

    def __init__(self, identificador, nombre, correo, telefono):
        """Inicializa un cliente y valida sus datos personales."""
        super().__init__(identificador)

        self.__nombre = self._validar_nombre(nombre)
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_nombre(nombre):
        """Comprueba que el nombre sea un texto válido y no esté vacío."""
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidationError("El nombre del cliente no es válido.")

        return nombre.strip()

    @staticmethod
    def _validar_correo(correo):
        """Comprueba que el correo tenga un formato básico válido."""
        if not isinstance(correo, str) or "@" not in correo:
            raise ValidationError("El correo electrónico no es válido.")

        if "." not in correo.split("@")[-1]:
            raise ValidationError("El dominio del correo no es válido.")

        return correo.strip().lower()

    @staticmethod
    def _validar_telefono(telefono):
        """Comprueba que el teléfono contenga al menos siete dígitos."""
        if not isinstance(telefono, str):
            raise ValidationError("El teléfono debe ser texto.")

        telefono = telefono.strip()

        if not telefono.isdigit() or len(telefono) < 7:
            raise ValidationError("El número de teléfono no es válido.")

        return telefono

    @property
    def nombre(self):
        """Devuelve el nombre del cliente."""
        return self.__nombre

    @property
    def correo(self):
        """Devuelve el correo electrónico del cliente."""
        return self.__correo

    @property
    def telefono(self):
        """Devuelve el número telefónico del cliente."""
        return self.__telefono

    def mostrar_informacion(self):
        """Devuelve los datos principales del cliente en formato de texto."""
        return (
            f"ID: {self.identificador}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}\n"
            f"Teléfono: {self.telefono}"
        )

    def __str__(self):
        """Devuelve una representación breve del cliente."""
        return f"Cliente: {self.nombre} ({self.identificador})"
