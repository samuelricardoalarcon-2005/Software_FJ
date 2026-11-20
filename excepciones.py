
"""Define las excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base para los errores propios del sistema."""
    pass


class ValidationError(SoftwareFJError):
    """Representa errores en la validación de datos ingresados."""
    pass


class ClientError(SoftwareFJError):
    """Representa errores relacionados con la gestión de clientes."""
    pass


class ServiceError(SoftwareFJError):
    """Representa errores relacionados con los servicios ofrecidos."""
    pass


class ReservationError(SoftwareFJError):
    """Representa errores durante la gestión de reservas."""
    pass


class AvailabilityError(ReservationError):
    """Indica que un servicio o recurso no está disponible."""
    pass
