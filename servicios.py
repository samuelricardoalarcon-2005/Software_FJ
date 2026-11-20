
"""Define los servicios disponibles en el sistema Software FJ."""

from abc import abstractmethod
from entidades import Entidad
from excepciones import ServiceError, ValidationError


class Servicio(Entidad):
    """Clase abstracta que establece la estructura común de los servicios."""

    def __init__(self, identificador, nombre, tarifa_base):
        """Inicializa un servicio y valida su nombre y tarifa."""
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidationError("El nombre del servicio es obligatorio.")

        if (
            not isinstance(tarifa_base, (int, float))
            or isinstance(tarifa_base, bool)
            or tarifa_base <= 0
        ):
            raise ValidationError("La tarifa base debe ser mayor que cero.")

        self._nombre = nombre.strip()
        self._tarifa_base = tarifa_base

    @property
    def nombre(self):
        """Devuelve el nombre del servicio."""
        return self._nombre

    @property
    def tarifa_base(self):
        """Devuelve la tarifa base del servicio."""
        return self._tarifa_base

    def mostrar_informacion(self):
        """Devuelve la información general del servicio."""
        return (
            f"ID: {self.identificador}\n"
            f"Servicio: {self.nombre}\n"
            f"Tarifa base: ${self.tarifa_base:,.0f}"
        )

    def _calcular_total(self, subtotal, descuento, impuesto):
        """Calcula el costo final aplicando descuento e impuesto."""
        if (
            not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not 0 <= descuento <= 1
        ):
            raise ServiceError("El descuento debe estar entre 0 y 1.")

        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or not 0 <= impuesto <= 1
        ):
            raise ServiceError("El impuesto debe estar entre 0 y 1.")

        total = subtotal * (1 - descuento)
        return round(total * (1 + impuesto), 2)

    @abstractmethod
    def validar_parametros(self, parametro):
        """Define la validación específica de cada tipo de servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion, parametro=1, descuento=0, impuesto=0):
        """Define el cálculo del costo según el tipo de servicio."""
        pass

    @abstractmethod
    def describir_servicio(self):
        """Define la descripción específica de cada servicio."""
        pass


class ReservaSala(Servicio):
    """Representa el servicio de reserva de salas por horas."""

    def __init__(self, identificador, capacidad, tarifa_hora):
        """Inicializa una sala y valida su capacidad."""
        super().__init__(identificador, "Reserva de sala", tarifa_hora)

        if (
            not isinstance(capacidad, int)
            or isinstance(capacidad, bool)
            or capacidad <= 0
        ):
            raise ValidationError("La capacidad de la sala debe ser positiva.")

        self._capacidad = capacidad

    def validar_parametros(self, personas):
        """Comprueba que la cantidad de personas no supere la capacidad."""
        if not isinstance(personas, int) or isinstance(personas, bool):
            raise ServiceError("La cantidad de personas debe ser un entero.")

        if personas <= 0 or personas > self._capacidad:
            raise ServiceError(
                "La cantidad de personas supera la capacidad de la sala."
            )

        return True

    def calcular_costo(self, duracion, parametro=1, descuento=0, impuesto=0):
        """Calcula el costo de reservar una sala según las horas utilizadas."""
        self.validar_parametros(parametro)

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):
            raise ServiceError("Las horas deben ser mayores que cero.")

        subtotal = self.tarifa_base * duracion
        return self._calcular_total(subtotal, descuento, impuesto)

    def describir_servicio(self):
        """Devuelve la descripción y capacidad de la sala."""
        return f"Sala con capacidad para {self._capacidad} personas."


class AlquilerEquipo(Servicio):
    """Representa el alquiler de equipos por días."""

    def __init__(self, identificador, unidades_disponibles, tarifa_dia):
        """Inicializa el alquiler y valida las unidades disponibles."""
        super().__init__(identificador, "Alquiler de equipos", tarifa_dia)

        if (
            not isinstance(unidades_disponibles, int)
            or isinstance(unidades_disponibles, bool)
            or unidades_disponibles <= 0
        ):
            raise ValidationError(
                "Las unidades disponibles deben ser positivas."
            )

        self._unidades_disponibles = unidades_disponibles

    def validar_parametros(self, cantidad):
        """Comprueba que la cantidad solicitada esté disponible."""
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise ServiceError("La cantidad debe ser un número entero.")

        if cantidad <= 0 or cantidad > self._unidades_disponibles:
            raise ServiceError("No hay suficientes equipos disponibles.")

        return True

    def calcular_costo(self, duracion, parametro=1, descuento=0, impuesto=0):
        """Calcula el costo del alquiler según días y cantidad de equipos."""
        self.validar_parametros(parametro)

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):
            raise ServiceError("Los días deben ser mayores que cero.")

        subtotal = self.tarifa_base * duracion * parametro
        return self._calcular_total(subtotal, descuento, impuesto)

    def describir_servicio(self):
        """Devuelve la descripción y cantidad de equipos disponibles."""
        return (
            f"Alquiler de equipos. "
            f"Unidades disponibles: {self._unidades_disponibles}."
        )


class AsesoriaEspecializada(Servicio):
    """Representa el servicio de asesorías especializadas por horas."""

    def __init__(self, identificador, especialidad, tarifa_hora):
        """Inicializa una asesoría y valida la especialidad."""
        super().__init__(
            identificador,
            "Asesoría especializada",
            tarifa_hora
        )

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValidationError("La especialidad es obligatoria.")

        self._especialidad = especialidad.strip()

    def validar_parametros(self, modalidad):
        """Comprueba que la modalidad sea virtual o presencial."""
        if not isinstance(modalidad, str):
            raise ServiceError("La modalidad debe ser texto.")

        if modalidad.lower() not in ("virtual", "presencial"):
            raise ServiceError("La modalidad debe ser virtual o presencial.")

        return True

    def calcular_costo(self, duracion, parametro="virtual", descuento=0, impuesto=0):
        """Calcula el costo de la asesoría según las horas contratadas."""
        self.validar_parametros(parametro)

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):
            raise ServiceError("Las horas deben ser mayores que cero.")

        subtotal = self.tarifa_base * duracion
        return self._calcular_total(subtotal, descuento, impuesto)

    def describir_servicio(self):
        """Devuelve la descripción de la asesoría y su especialidad."""
        return f"Asesoría especializada en {self._especialidad}."
