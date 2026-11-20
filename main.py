
"""Ejecuta las pruebas de funcionamiento del sistema Software FJ."""

from entidades import Cliente
from servicios import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)
from reservas import Reserva

from excepciones import (
    SoftwareFJError,
    ValidationError,
    ServiceError,
    ReservationError
)

from registro import (
    registrar_evento,
    registrar_error,
    registrar_excepcion
)


def ejecutar_pruebas():
    """Ejecuta las operaciones y pruebas de validación del sistema."""

    print("==========================================")
    print("          SISTEMA SOFTWARE FJ")
    print("          PRUEBAS DE FUNCIONAMIENTO")
    print("==========================================")

    # OPERACION 1: Registro correcto de cliente
    print("\n1. REGISTRO DE CLIENTE")

    cliente = Cliente(
        "C001",
        "Samuel Torres",
        "samuel@gmail.com",
        "3001234567"
    )

    print("Cliente registrado:", cliente.nombre)
    registrar_evento("Operacion 1: Cliente registrado.")

    # OPERACION 2: Cliente con correo inválido
    print("\n2. VALIDACION DE CLIENTE")

    try:
        Cliente(
            "C002",
            "Cliente Prueba",
            "correo_invalido",
            "3001234567"
        )

    except ValidationError as error:
        print("Error controlado:", error)
        registrar_error(f"Operacion 2: {error}")

    # OPERACION 3: Crear sala
    print("\n3. CREACION DE SALA")

    sala = ReservaSala("S001", 20, 50000)

    print(sala.describir_servicio())
    registrar_evento("Operacion 3: Sala creada.")

    # OPERACION 4: Servicio con capacidad inválida
    print("\n4. VALIDACION DE SERVICIO")

    try:
        ReservaSala("S002", 0, 50000)

    except ValidationError as error:
        print("Error controlado:", error)
        registrar_error(f"Operacion 4: {error}")

    # OPERACION 5: Crear alquiler
    print("\n5. CREACION DE ALQUILER")

    equipo = AlquilerEquipo("E001", 10, 30000)

    print(equipo.describir_servicio())
    registrar_evento("Operacion 5: Alquiler creado.")

    # OPERACION 6: Crear asesoría
    print("\n6. CREACION DE ASESORIA")

    asesoria = AsesoriaEspecializada(
        "A001",
        "Programacion",
        60000
    )

    print(asesoria.describir_servicio())
    registrar_evento("Operacion 6: Asesoria creada.")

    # OPERACION 7: Crear reserva
    print("\n7. CREACION DE RESERVA")

    reserva = Reserva("R001", cliente, sala, 2, 5)

    print("Reserva creada:", reserva.identificador)
    registrar_evento("Operacion 7: Reserva creada.")

    # OPERACION 8: Confirmar y procesar
    print("\n8. CONFIRMACION Y PROCESAMIENTO")

    print(reserva.confirmar())

    costo = reserva.procesar(
        descuento=0.10,
        impuesto=0.19
    )

    print(f"Costo final: ${costo:,.2f}")
    registrar_evento(
        f"Operacion 8: Reserva procesada. Costo: ${costo:,.2f}"
    )

    # OPERACION 9: Superar capacidad de sala
    print("\n9. VALIDACION DE DISPONIBILIDAD")

    try:
        sala.validar_parametros(30)

    except ServiceError as error:
        print("Error controlado:", error)
        registrar_error(f"Operacion 9: {error}")

    # OPERACION 10: Confirmar reserva procesada
    print("\n10. VALIDACION DEL ESTADO")

    try:
        reserva.confirmar()

    except ReservationError as error:
        print("Error controlado:", error)
        registrar_error(f"Operacion 10: {error}")

    # OPERACION 11: Intentar crear una reserva inválida
    print("\n11. CREACION DE RESERVA INVALIDA")

    try:
        Reserva("R002", cliente, sala, 2, 30)

    except SoftwareFJError as error:
        print("Reserva rechazada:", error)
        registrar_error(f"Operacion 11: {error}")

    # OPERACION 12: Comprobar excepciones encadenadas
    print("\n12. PRUEBA DE EXCEPCIONES ENCADENADAS")

    reserva_prueba = Reserva("R003", cliente, sala, 2, 5)
    reserva_prueba.confirmar()

    try:
        reserva_prueba.procesar(descuento=1.5)

    except ReservationError as error:
        print("Error de procesamiento:", error)

        if error.__cause__ is not None:
            print("Causa original:", error.__cause__)

        registrar_excepcion(
            "Operacion 12: Excepcion encadenada durante el procesamiento."
        )

    # OPERACION 13: Cancelar una reserva pendiente
    print("\n13. CANCELACION DE RESERVA")

    reserva_cancelacion = Reserva("R004", cliente, sala, 1, 5)

    print(reserva_cancelacion.cancelar())
    print("Estado:", reserva_cancelacion.estado)

    registrar_evento(
        "Operacion 13: Reserva cancelada correctamente."
    )

    # Resumen final
    print("\n==========================================")
    print("             RESUMEN FINAL")
    print("==========================================")

    print(reserva.mostrar_informacion())

    print("\nLas pruebas finalizaron correctamente.")

    registrar_evento("Todas las pruebas finalizaron.")


if __name__ == "__main__":

    try:
        ejecutar_pruebas()

    except SoftwareFJError as error:
        registrar_error(f"Error general del sistema: {error}")
        print("\nError del sistema:", error)

    except Exception:
        registrar_excepcion("Se produjo un error inesperado.")
        print("\nError inesperado. Consultar el archivo de registros.")

    else:
        print("\nEjecucion finalizada correctamente.")

    finally:
        registrar_evento("Finalizo la ejecucion del programa.")
        print("\nFin del programa.")
