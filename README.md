# Taxímetro
Prototipo de taxímetro en CLI, desarrollado de forma incremental en 4 fases.

## Estado del proyecto
- [x] Fase 1 — MVP funcional (CLI)
- [ ] Fase 2 — Observabilidad y persistencia
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
| `salir` — cierra el programa | `m` — cambia a estado en movimiento |
| | `fin` — finaliza y muestra el importe total |

Mientras una carrera está activa, el sistema muestra automáticamente el tiempo transcurrido, el estado y el importe acumulado cada 3 segundos, sin necesidad de pulsar ninguna tecla.

## Limitación conocida (Fase 1)

Al combinar un `input()` bloqueante con un hilo que imprime el estado en segundo plano, el mensaje periódico de estado puede aparecer intercalado de forma poco prolija con el `>` del prompt. Es una limitación conocida de una interfaz de terminal simple, no un error. Se resuelve de raíz en la Fase 3 con una interfaz gráfica no bloqueante.

## Cómo ejecutar los Tests

_Pendiente: se añadirán en la Fase 2 (US-07 pide explícitamente cobertura de tests para el cálculo de tarifas)._

## Arquitectura

```
taximetro/
├── __init__.py
├── config.py    # Tarifas (fijas en Fase 1)
├── core.py      # Clase Ride: estado, hilo de acumulación en tiempo real
└── cli.py       # Interfaz de terminal: lee comandos, no calcula nada
main.py          # Punto de entrada
```

Principio de diseño: `core.py` no sabe que existe una terminal. `cli.py` solo llama a métodos públicos de `Ride` (`start`, `change_state`, `finish`, `current_status`) — nunca calcula tarifas por su cuenta. Esto permitirá añadir una GUI (Fase 3) o una API (Fase 4) sin tocar la lógica de negocio.

## Tarifas vigentes (Zona EMT Madrid, Septiembre 2026)

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

Los cambios se aplican en el **siguiente arranque** del programa (no en caliente, mientras ya se está ejecutando). Si el fichero no existe o está mal formado, el sistema usa automáticamente unos valores por defecto y registra el problema en el log — nunca se cae por un fichero de configuración incorrecto.

## Convenciones
- Tablero de tareas en GitHub Projects, a partir de la Fase 2.
