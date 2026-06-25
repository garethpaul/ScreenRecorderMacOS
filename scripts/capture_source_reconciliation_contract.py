#!/usr/bin/env python3


def validation_errors(source):
    errors = []

    helper_fragments = [
        "private func refreshedSelection<Element, Identifier: Equatable>(",
        "guard let current else { return available.first }",
        "let currentIdentifier = identifier(current)",
        "return available.first { identifier($0) == currentIdentifier } ?? available.first",
    ]
    for fragment in helper_fragments:
        if fragment not in source:
            errors.append(f"capture source reconciliation must preserve {fragment}")

    property_fragments = [
        "if oldValue?.displayID != selectedDisplay?.displayID { updateEngine() }",
        "if oldValue?.windowID != selectedWindow?.windowID { updateEngine() }",
    ]
    for fragment in property_fragments:
        if fragment not in source:
            errors.append(f"capture source identity changes must preserve {fragment}")

    refresh_fragments = [
        "selectedDisplay = refreshedSelection(\n"
        "                current: selectedDisplay,\n"
        "                available: availableDisplays,\n"
        "                identifier: { $0.displayID }\n"
        "            )",
        "selectedWindow = refreshedSelection(\n"
        "                current: selectedWindow,\n"
        "                available: availableWindows,\n"
        "                identifier: { $0.windowID }\n"
        "            )",
    ]
    for fragment in refresh_fragments:
        if fragment not in source:
            errors.append("capture refresh must replace missing or stale selected sources by stable identifier")

    for stale_pattern in [
        "if selectedDisplay == nil {",
        "if selectedWindow == nil {",
    ]:
        if stale_pattern in source:
            errors.append(f"capture refresh must not retain nil-only reconciliation: {stale_pattern}")

    return errors
