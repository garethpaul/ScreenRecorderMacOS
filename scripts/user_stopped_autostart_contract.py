#!/usr/bin/env python3


def validation_errors(source):
    appearance_start = source.rfind(".onAppear {")
    if appearance_start < 0:
        return ["ContentView must retain its appearance task"]

    appearance = source[appearance_start:]
    permission_guard = "if await screenRecorder.canRecord {"
    stop_guard = "if !userStopped {"
    capture_start = "await screenRecorder.start()"
    unauthorized_branch = "} else {"
    required = (permission_guard, stop_guard, capture_start, unauthorized_branch)
    positions = [appearance.find(fragment) for fragment in required]

    if (
        any(position < 0 for position in positions)
        or positions != sorted(positions)
        or appearance.count(capture_start) != 1
    ):
        return [
            "ContentView must honor persisted stop intent before authorized appearance auto-start"
        ]

    return []
