#!/usr/bin/env python3
from pathlib import Path

from screen_recorder_start_stop_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "CaptureSample" / "ScreenRecorder.swift").read_text(
    encoding="utf-8"
)

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline screen recorder start/stop contract invalid: {errors}")

mutations = {
    "start guard omits active start": baseline.replace(
        "guard !isRunning, !isStartTaskActive, !isStopTaskActive else { return }",
        "guard !isRunning, !isStopTaskActive else { return }",
        1,
    ),
    "start guard omits active stop": baseline.replace(
        "guard !isRunning, !isStartTaskActive, !isStopTaskActive else { return }",
        "guard !isRunning, !isStartTaskActive else { return }",
        1,
    ),
    "start task flag set after await": baseline.replace(
        "isStartTaskActive = true\n        defer { isStartTaskActive = false }",
        "defer { isStartTaskActive = false }",
        1,
    ).replace(
        "await monitorAvailableContent()",
        "await monitorAvailableContent()\n            isStartTaskActive = true",
        1,
    ),
    "stop guard omits active stop": baseline.replace(
        "guard isRunning, !isStopTaskActive else { return }",
        "guard isRunning else { return }",
        1,
    ),
    "stop task flag set after await": baseline.replace(
        "isStopTaskActive = true\n"
        "        defer { isStopTaskActive = false }\n\n"
        "        await captureEngine.stopCapture()",
        "await captureEngine.stopCapture()\n"
        "        isStopTaskActive = true\n"
        "        defer { isStopTaskActive = false }",
        1,
    ),
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(
    "Screen recorder start/stop contract passed "
    f"({len(mutations)} mutations rejected)."
)
