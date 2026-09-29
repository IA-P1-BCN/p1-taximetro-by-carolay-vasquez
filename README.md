# Taxímetro
Prototipo de taxímetro en CLI, desarrollado de forma incremental en 4 fases.

## Estado del proyecto

- [x] Fase 1 — MVP funcional (CLI)
- [x] Fase 2 — Observabilidad y persistencia
- [ ] Fase 3 — Arquitectura y experiencia de usuario
- [ ] Fase 4 — Versión de producción

## Cómo ejecutarlo

```bash
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

python main.py
```

Comandos disponibles:

| Fuera de una carrera | Durante una carrera |
|---|---|
| `iniciar` — arranca una nueva carrera | `p` — cambia a estado parado |
| `historial` — muestra las carreras registradas | `m` — cambia a estado en movimiento |
| `salir` — cierra el programa | `fin` — finaliza y muestra el importe total |

Mientras una carrera está activa, el sistema muestra automáticamente el tiempo transcurrido, el estado y el importe acumulado cada 2.5 segundos, sin necesidad de pulsar ninguna tecla.

## Limitación conocida (Fase 1)

Al combinar un `input()` bloqueante con un hilo que imprime el estado en segundo plano, el mensaje periódico de estado puede aparecer intercalado de forma poco prolija con el `>` del prompt. Es una limitación conocida de una interfaz de terminal simple, no un error. Se resuelve de raíz en la Fase 3 con una interfaz gráfica no bloqueante.

## Cómo ejecutar los tests

```bash
python -m unittest discover -s tests -t .
```

Cubren `rate_for_state()` y `fare_for_segment()` en `core.py`: los casos de tarifa parado/movimiento, tramos de 0, 3 y 2.5 segundos, y el caso de error con un estado desconocido.

## Arquitectura

```
config/
└── rates.json          # Tarifas editables sin tocar código (Fase 2)
taximetro/
├── __init__.py
├── config.py            # Carga rates.json, con valores por defecto de respaldo
├── core.py               # Clase Ride: estado, hilo de acumulación en tiempo real
├── history.py             # Persistencia del historial de carreras (JSON)
├── logging_config.py       # Configuración centralizada de logging
└── cli.py                   # Interfaz de terminal: lee comandos, no calcula nada
tests/
└── test_core.py                # Tests de la lógica de cálculo de tarifas
main.py                          # Punto de entrada
```

Principio de diseño: `core.py` no sabe que existe una terminal. `cli.py` solo llama a métodos públicos de `Ride` (`start`, `change_state`, `finish`, `current_status`) — nunca calcula tarifas por su cuenta. Esto permitirá añadir una GUI (Fase 3) o una API (Fase 4) sin tocar la lógica de negocio.

## Tarifas vigentes (Zona EMT Madrid, junio 2025)

| Estado del taxi | Tarifa |
|---|---|
| Parado o < 20 km/h | 0.02 €/segundo |
| En movimiento | 0.05 €/segundo |

## Cómo modificar las tarifas

Las tarifas se leen de `config/rates.json`, no están escritas en el código. Para cambiarlas, edita ese fichero:

```json
{
  "stopped": 0.02,
  "moving": 0.05
}
```

Los cambios se aplican en el **siguiente arranque** del programa (no en caliente, mientras ya está corriendo). Si el fichero no existe o está mal formado, el sistema usa automáticamente unos valores por defecto y registra el problema en el log — nunca se cae por un fichero de configuración incorrecto.


## Logs de operación
Cada ejecución escribe en `taximetro.log` (en la raíz del proyecto): arranque y cierre de la aplicación, cada cambio de estado de una carrera, el cierre de una carrera con su duración e importe, y cualquier error (por ejemplo, un estado desconocido). El fichero no se versiona (está en `.gitignore`) porque es un dato de cada máquina, no código fuente.


## Historial de carreras
Cada carrera finalizada se guarda automáticamente en `history.json` (en la raíz del proyecto), con fecha, duración e importe. Se consulta desde la propia CLI con el comando `historial`, y persiste entre sesiones sin ninguna acción manual — cerrar y volver a abrir el programa no borra los datos. Tampoco se versiona, por la misma razón que el log.


## Convenciones
- Tablero de tareas en GitHub Projects, a partir de la Fase 2.
