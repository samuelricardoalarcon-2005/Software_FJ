
"""Administra los clientes, servicios y reservas de Software FJ."""

from entidades import Cliente
from servicios import Servicio
from reservas import Reserva

from excepciones import (
    ClientError,
    ServiceError,
    ReservationError,
    SoftwareFJError
)

from registro import registrar_evento, registrar_error


class SistemaSoftwareFJ:
    """Gestiona los registros del sistema mediante listas internas."""

    def __init__(self):
        """Inicializa las listas que almacenan los objetos del sistema."""
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    def registrar_cliente(self, cliente):
        """Registra un cliente después de validar que no esté duplicado."""
        try:
            if not isinstance(cliente, Cliente):
                raise ClientError(
                    "El objeto proporcionado no es un cliente."
                )

            if any(
                c.identificador == cliente.identificador
                for c in self.__clientes
            ):
                raise ClientError(
                    "Ya existe un cliente con ese identificador."
                )

            self.__clientes.append(cliente)

            registrar_evento(
                f"Cliente {cliente.identificador} registrado en el sistema."
            )

            return cliente

        except SoftwareFJError as error:
            registrar_error(f"Error al registrar cliente: {error}")
            raise

    def registrar_servicio(self, servicio):
        """Registra un servicio y evita identificadores duplicados."""
        try:
            if not isinstance(servicio, Servicio):
                raise ServiceError(
                    "El objeto proporcionado no es un servicio."
                )

            if any(
                s.identificador == servicio.identificador
                for s in self.__servicios
            ):
                raise ServiceError(
                    "Ya existe un servicio con ese identificador."
                )

            self.__servicios.append(servicio)

            registrar_evento(
                f"Servicio {servicio.identificador} registrado en el sistema."
            )

            return servicio

        except SoftwareFJError as error:
            registrar_error(f"Error al registrar servicio: {error}")
            raise

    def registrar_reserva(self, reserva):
        """Registra una reserva existente y evita identificadores duplicados."""
        try:
            if not isinstance(reserva, Reserva):
                raise ReservationError(
                    "El objeto proporcionado no es una reserva."
                )

            if any(
                r.identificador == reserva.identificador
                for r in self.__reservas
            ):
                raise ReservationError(
                    "Ya existe una reserva con ese identificador."
                )

            self.__reservas.append(reserva)

            registrar_evento(
                f"Reserva {reserva.identificador} registrada en el sistema."
            )

            return reserva

        except SoftwareFJError as error:
            registrar_error(f"Error al registrar reserva: {error}")
            raise

    def buscar_cliente(self, identificador):
        """Busca un cliente por su identificador."""
        for cliente in self.__clientes:
            if cliente.identificador == identificador:
                return cliente

        raise ClientError(
            "No se encontró el cliente solicitado."
        )

    def buscar_servicio(self, identificador):
        """Busca un servicio por su identificador."""
        for servicio in self.__servicios:
            if servicio.identificador == identificador:
                return servicio

        raise ServiceError(
            "No se encontró el servicio solicitado."
        )

    def buscar_reserva(self, identificador):
        """Busca una reserva por su identificador."""
        for reserva in self.__reservas:
            if reserva.identificador == identificador:
                return reserva

        raise ReservationError(
            "No se encontró la reserva solicitada."
        )

    def crear_reserva(
        self,
        identificador,
        id_cliente,
        id_servicio,
        duracion,
        parametro=1
    ):
        """Crea y almacena una reserva usando registros existentes."""
        try:
            if any(
                r.identificador == identificador
                for r in self.__reservas
            ):
                raise ReservationError(
                    "Ya existe una reserva con ese identificador."
                )

            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)

            reserva = Reserva(
                identificador,
                cliente,
                servicio,
                duracion,
                parametro
            )

            self.registrar_reserva(reserva)

            return reserva

        except SoftwareFJError as error:
            registrar_error(f"Error al crear reserva: {error}")
            raise

    def listar_clientes(self):
        """Devuelve una copia de la lista de clientes."""
        return self.__clientes.copy()

    def listar_servicios(self):
        """Devuelve una copia de la lista de servicios."""
        return self.__servicios.copy()

    def listar_reservas(self):
        """Devuelve una copia de la lista de reservas."""
        return self.__reservas.copy()

    def mostrar_resumen(self):
        """Devuelve la cantidad de registros almacenados."""
        return (
            f"Clientes registrados: {len(self.__clientes)}\n"
            f"Servicios registrados: {len(self.__servicios)}\n"
            f"Reservas registradas: {len(self.__reservas)}"
        )
