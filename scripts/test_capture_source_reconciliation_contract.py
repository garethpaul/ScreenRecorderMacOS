#!/usr/bin/env python3
from pathlib import Path

from capture_source_reconciliation_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "CaptureSample" / "ScreenRecorder.swift").read_text(encoding="utf-8")

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline capture source reconciliation invalid: {errors}")

mutations = {
    "display identity guard removed": baseline.replace(
        "if oldValue?.displayID != selectedDisplay?.displayID { updateEngine() }",
        "updateEngine()",
        1,
    ),
    "window identity guard removed": baseline.replace(
        "if oldValue?.windowID != selectedWindow?.windowID { updateEngine() }",
        "updateEngine()",
        1,
    ),
    "display reconciliation removed": baseline.replace(
        "            selectedDisplay = refreshedSelection(\n"
        "                current: selectedDisplay,\n"
        "                available: availableDisplays,\n"
        "                identifier: { $0.displayID }\n"
        "            )\n",
        "",
        1,
    ),
    "window reconciliation removed": baseline.replace(
        "            selectedWindow = refreshedSelection(\n"
        "                current: selectedWindow,\n"
        "                available: availableWindows,\n"
        "                identifier: { $0.windowID }\n"
        "            )\n",
        "",
        1,
    ),
    "first-source fallback removed": baseline.replace(
        "return available.first { identifier($0) == currentIdentifier } ?? available.first",
        "return available.first { identifier($0) == currentIdentifier }",
        1,
    ),
    "nil-only display reconciliation restored": baseline.replace(
        "            selectedDisplay = refreshedSelection(\n"
        "                current: selectedDisplay,\n"
        "                available: availableDisplays,\n"
        "                identifier: { $0.displayID }\n"
        "            )\n",
        "            if selectedDisplay == nil {\n"
        "                selectedDisplay = availableDisplays.first\n"
        "            }\n",
        1,
    ),
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(f"Capture source reconciliation contract passed ({len(mutations)} mutations rejected).")
