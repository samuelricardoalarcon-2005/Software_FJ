
"""Gestiona las reservas realizadas por los clientes de Software FJ."""

from excepciones import ReservationError, SoftwareFJError, ValidationError


class Reserva:
    """Representa una reserva asociada a un cliente y un servicio."""

    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Cancelada", "Procesada")

    def __init__(self, identificador, cliente, servicio, duracion, parametro=1):
        """Crea una reserva y valida sus datos iniciales."""

        if not isinstance(identificador, str) or not identificador.strip():
            raise ValidationError("El identificador de la reserva es obligatorio.")

        if cliente is None:
            raise ReservationError("La reserva necesita un cliente.")

        if servicio is None:
            raise ReservationError("La reserva necesita un servicio.")

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):
            raise ReservationError("La duración debe ser mayor que cero.")

        servicio.validar_parametros(parametro)

        self._identificador = identificador.strip()
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._parametro = parametro
        self._estado = "Pendiente"
        self._costo = 0

    @property
    def identificador(self):
        """Devuelve el identificador de la reserva."""
        return self._identificador

    @property
    def cliente(self):
        """Devuelve el cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self):
        """Devuelve el servicio asociado a la reserva."""
        return self._servicio

    @property
    def estado(self):
        """Devuelve el estado actual de la reserva."""
        return self._estado

    @property
    def costo(self):
        """Devuelve el costo calculado de la reserva."""
        return self._costo

    def confirmar(self):
        """Confirma una reserva que se encuentra pendiente."""
        if self._estado != "Pendiente":
            raise ReservationError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self._estado = "Confirmada"
        return "Reserva confirmada correctamente."

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""
        if self._estado not in ("Pendiente", "Confirmada"):
            raise ReservationError("Esta reserva no puede cancelarse.")

        self._estado = "Cancelada"
        return "Reserva cancelada correctamente."

    def procesar(self, descuento=0, impuesto=0):
        """Calcula el costo de una reserva confirmada y cambia su estado."""
        if self._estado != "Confirmada":
            raise ReservationError(
                "La reserva debe estar confirmada antes de procesarse."
            )

        try:
            self._costo = self._servicio.calcular_costo(
                self._duracion,
                self._parametro,
                descuento,
                impuesto
            )

        except SoftwareFJError as error:
            raise ReservationError(
                "No fue posible procesar el costo de la reserva."
            ) from error

        self._estado = "Procesada"
        return self._costo

    def mostrar_informacion(self):
        """Devuelve los datos principales de la reserva."""
        return (
            f"Reserva: {self._identificador}\n"
            f"Cliente: {self._cliente.nombre}\n"
            f"Servicio: {self._servicio.nombre}\n"
            f"Duración: {self._duracion}\n"
            f"Estado: {self._estado}\n"
            f"Costo: ${self._costo:,.2f}"
        )

    def __str__(self):
        """Devuelve una representación breve de la reserva."""
        return (
            f"Reserva {self._identificador} - "
            f"{self._cliente.nombre} - {self._estado}"
        )
