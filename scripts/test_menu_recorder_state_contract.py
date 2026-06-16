#!/usr/bin/env python3
from pathlib import Path

from menu_recorder_state_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "CaptureSample" / "Views" / "MenuView.swift").read_text(
    encoding="utf-8"
)

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline menu view invalid: {errors}")

mutations = {
    "persisted intent chooses operation": baseline.replace(
        "if screenRecorder.isRunning {", "if userStopped {", 1
    ),
    "inverted stop intent": baseline.replace(
        "self.userStopped = true", "self.userStopped = false", 1
    ),
    "stop intent after task": baseline.replace(
        "self.userStopped = true\n                            Task {\n"
        "                                await screenRecorder.stop()\n"
        "                            }",
        "Task {\n                                await screenRecorder.stop()\n"
        "                            }\n                            self.userStopped = true",
        1,
    ),
    "inverted start intent": baseline.replace(
        "self.userStopped = false", "self.userStopped = true", 1
    ),
    "start intent after task": baseline.replace(
        "self.userStopped = false\n                            Task {\n"
        "                                await screenRecorder.start()\n"
        "                            }",
        "Task {\n                                await screenRecorder.start()\n"
        "                            }\n                            self.userStopped = false",
        1,
    ),
    "duplicate start": baseline.replace(
        "await screenRecorder.start()",
        "await screenRecorder.start()\n                                await screenRecorder.start()",
        1,
    ),
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(f"Menu recorder-state contract passed ({len(mutations)} mutations rejected).")
