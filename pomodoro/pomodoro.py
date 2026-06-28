#!/usr/bin/env python3
"""Pomodoro Terminal — timer con barra de progreso animada."""

import time
import sys
import os
import json
from datetime import datetime

SESSIONS_FILE = os.path.join(os.path.dirname(__file__), "sessions.json")

WORK_MINUTES = 25
SHORT_BREAK = 5
LONG_BREAK = 15
SESSIONS_BEFORE_LONG = 4

COLORS = {
    "red":    "\033[91m",
    "green":  "\033[92m",
    "yellow": "\033[93m",
    "cyan":   "\033[96m",
    "bold":   "\033[1m",
    "reset":  "\033[0m",
    "clear":  "\033[2J\033[H",
}

def c(color, text):
    return f"{COLORS[color]}{text}{COLORS['reset']}"

def beep(times=1):
    for _ in range(times):
        print("\a", end="", flush=True)
        time.sleep(0.3)

def load_sessions():
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE) as f:
            return json.load(f)
    return {"total": 0, "today": 0, "last_date": ""}

def save_sessions(data):
    today = datetime.now().strftime("%Y-%m-%d")
    if data["last_date"] != today:
        data["today"] = 0
        data["last_date"] = today
    data["total"] += 1
    data["today"] += 1
    with open(SESSIONS_FILE, "w") as f:
        json.dump(data, f)
    return data

def draw_bar(elapsed, total, width=40):
    pct = elapsed / total
    filled = int(pct * width)
    bar = "█" * filled + "░" * (width - filled)
    return bar, pct

def countdown(label, color, minutes, session_data):
    total_secs = minutes * 60
    start = time.time()

    try:
        while True:
            elapsed = time.time() - start
            remaining = total_secs - elapsed
            if remaining <= 0:
                remaining = 0

            bar, pct = draw_bar(elapsed, total_secs)
            mins = int(remaining) // 60
            secs = int(remaining) % 60

            sessions_str = c("cyan", f"Hoy: {session_data['today']}  Total: {session_data['total']}")

            print(COLORS["clear"], end="")
            print()
            print(c("bold", f"  🍅 POMODORO TERMINAL"))
            print()
            print(f"  {c(color, label)}")
            print()
            print(f"  {c(color, bar)}  {pct*100:.0f}%")
            print()
            print(f"  ⏱  {c('bold', f'{mins:02d}:{secs:02d}')} restantes")
            print()
            print(f"  {sessions_str}")
            print()
            print(c("yellow", "  [Ctrl+C para pausar / salir]"))

            if remaining == 0:
                break

            time.sleep(0.5)

    except KeyboardInterrupt:
        print()
        print(c("yellow", "\n  ⏸  Pausado. Presiona Enter para continuar o Ctrl+C para salir."))
        try:
            input()
            # Reanudar con el tiempo restante
            remaining_at_pause = total_secs - (time.time() - start)
            if remaining_at_pause > 0:
                countdown(label, color, remaining_at_pause / 60, session_data)
                return
        except KeyboardInterrupt:
            print(c("red", "\n\n  Hasta luego 👋\n"))
            sys.exit(0)

def main():
    session_data = load_sessions()

    print(COLORS["clear"])
    print(c("bold", "  🍅 POMODORO TERMINAL"))
    print()
    print("  Técnica Pomodoro:")
    print(f"  • {c('green', f'{WORK_MINUTES} min')} de trabajo concentrado")
    print(f"  • {c('cyan', f'{SHORT_BREAK} min')} de descanso corto")
    print(f"  • {c('yellow', f'{LONG_BREAK} min')} de descanso largo cada {SESSIONS_BEFORE_LONG} pomodoros")
    print()

    today = datetime.now().strftime("%Y-%m-%d")
    if session_data["last_date"] != today:
        session_data["today"] = 0

    print(f"  Sesiones hoy: {c('cyan', str(session_data['today']))}  |  Total histórico: {c('cyan', str(session_data['total']))}")
    print()
    print(c("green", "  Presiona Enter para empezar..."))
    try:
        input()
    except KeyboardInterrupt:
        sys.exit(0)

    session_num = 0

    while True:
        session_num += 1
        session_data = load_sessions()

        # Trabajo
        print(COLORS["clear"])
        print(c("green", f"\n  🎯 Pomodoro #{session_num} — ¡a concentrarse!"))
        time.sleep(1.5)
        countdown("CONCENTRACIÓN", "green", WORK_MINUTES, session_data)

        session_data = save_sessions(session_data)
        beep(3)

        print(COLORS["clear"])
        print()
        print(c("bold", f"  ✅ ¡Pomodoro #{session_num} completado!"))
        print(f"  Sesiones hoy: {c('cyan', str(session_data['today']))}  |  Total: {c('cyan', str(session_data['total']))}")
        print()

        # Descanso
        if session_num % SESSIONS_BEFORE_LONG == 0:
            print(c("yellow", f"  🏖  ¡Descanso largo! {LONG_BREAK} minutos bien ganados."))
            time.sleep(2)
            countdown("DESCANSO LARGO", "yellow", LONG_BREAK, session_data)
        else:
            print(c("cyan", f"  ☕  Descanso corto de {SHORT_BREAK} minutos."))
            time.sleep(2)
            countdown("DESCANSO CORTO", "cyan", SHORT_BREAK, session_data)

        beep(2)
        print(COLORS["clear"])
        print(c("green", "\n  Descanso terminado. Presiona Enter para el siguiente pomodoro..."))
        try:
            input()
        except KeyboardInterrupt:
            print(c("red", "\n\n  Hasta luego 👋\n"))
            sys.exit(0)

if __name__ == "__main__":
    main()
