import threading
import time
import logging
 
from . import core

logger = logging.getLogger(__name__)
 
STATUS_INTERVAL_SECONDS = 2.5


def _print_status_periodically(ride: core.Ride):
    while ride.active:
        time.sleep(STATUS_INTERVAL_SECONDS)
        if not ride.active:
            break
        state, fare, duration = ride.current_status()
        print(
            f"\n[Tiempo: {duration:.0f}s | Estado: {state} | "
            f"Importe actual: {fare:.2f} EUR]"
        )


def show_instructions():
    print("=" * 60)
    print(" " * 15 + "¡Bienvenido al TAXIMETRO!")
    print("=" * 60)
    print("Fuera de una carrera:")
    print("  iniciar -> Iniciar una nueva carrera")
    print("  salir   -> Cerrar el programa")
    print()
    print("Durante una carrera:")
    print("  p       -> Cambiar a estado PARADO")
    print("  m       -> Cambiar a estado EN MOVIMIENTO")
    print("  fin     -> Finalizar la carrera y mostrar el importe total")
    print("=" * 60)
    print()


def ride_loop(ride: core.Ride):
    #Handles commands while a single ride is active.
    print("\nCarrera iniciada. Estado inicial: parado.")
    status_thread = threading.Thread(
        target=_print_status_periodically, args=(ride,), daemon=True
    )
    status_thread.start()
    while ride.active:
        command = input("\n> ").strip().lower()
        if command == "p":
            ride.change_state(core.STATE_STOPPED)
        elif command == "m":
            ride.change_state(core.STATE_MOVING)
        elif command == "fin":
            total = ride.finish()
            duration = ride.duration_seconds()
            print(
                f"\nCarrera finalizada. Duracion: {duration:.0f}s | "
                f"TOTAL A COBRAR: {total:.2f} EUR\n"
            )
        else:
            logger.warning("Unrecognized command during ride: %r", command)
            print("Comando no reconocido. Usa 'p', 'm' o 'fin'.")



def main():
    #Entry point for the whole CLI: the outer loop between rides.
    logger.info("Application started")
    show_instructions()
    while True:
        command = input("> ").strip().lower()
        if command == "iniciar":
            ride = core.Ride()
            ride.start()
            ride_loop(ride)
        elif command == "salir":
            logger.info("Application closed by user")
            print("Cerrando el taximetro. Buen turno.")
            break
        else:
            logger.warning("Unrecognized command: %r", command)
            print("Comando no reconocido. Usa 'iniciar' o 'salir'.")
