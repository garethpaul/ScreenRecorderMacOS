#!/usr/bin/env python3
from pathlib import Path

from user_stopped_autostart_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "CaptureSample" / "ContentView.swift").read_text(encoding="utf-8")
guard = "                    if !userStopped {\n"
start = "                        await screenRecorder.start()\n"
close = "                    }\n"

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline content view invalid: {errors}")

mutations = {
    "missing stop guard": baseline.replace(guard + start + close, start, 1),
    "inverted stop guard": baseline.replace("if !userStopped {", "if userStopped {", 1),
    "stop guard after start": baseline.replace(
        guard + start,
        start + guard,
        1,
    ),
    "duplicate unguarded start": baseline.replace(
        close + "                } else {",
        close + "                    await screenRecorder.start()\n                } else {",
        1,
    ),
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(f"Persisted stop autostart contract passed ({len(mutations)} mutations rejected).")
