# 🍅 Pomodoro Terminal

Timer Pomodoro con barra de progreso animada en la terminal.

## Uso

```bash
python3 pomodoro.py
```

Presiona **Enter** para iniciar cada sesión. Durante el temporizador:
- **Ctrl+C** → pausa (presiona Enter para reanudar, Ctrl+C de nuevo para salir)

## Ciclo

| Fase             | Duración |
|------------------|----------|
| Concentración    | 25 min   |
| Descanso corto   | 5 min    |
| Descanso largo   | 15 min (cada 4 pomodoros) |

El historial de sesiones se guarda automáticamente en `sessions.json`.
