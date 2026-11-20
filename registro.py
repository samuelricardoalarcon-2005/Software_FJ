
"""Configura y administra el registro de eventos y errores de Software FJ."""

import logging
import os


# Crear la carpeta de registros si no existe.
os.makedirs("logs", exist_ok=True)

# Configurar el archivo donde se almacenarán los eventos.
logging.basicConfig(
    filename="logs/software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    force=True
)

logger = logging.getLogger("SoftwareFJ")


def registrar_evento(mensaje):
    """Guarda una operación exitosa en el archivo de registros."""
    logger.info(mensaje)


def registrar_error(mensaje):
    """Guarda un error controlado en el archivo de registros."""
    logger.error(mensaje)


def registrar_excepcion(mensaje):
    """Guarda un error junto con los detalles de su excepción."""
    logger.exception(mensaje)
