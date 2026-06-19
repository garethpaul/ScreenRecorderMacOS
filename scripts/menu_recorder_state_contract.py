#!/usr/bin/env python3


def validation_errors(source):
    action_start = source.find("Button{")
    action_end = source.find("} label:", action_start)
    if action_start < 0 or action_end < 0:
        return ["MenuView must retain its recording button action"]

    action = source[action_start:action_end]
    required = (
        "if screenRecorder.isRunning {",
        "self.userStopped = true",
        "await screenRecorder.stop()",
        "} else {",
        "self.userStopped = false",
        "await screenRecorder.start()",
    )
    positions = [action.find(fragment) for fragment in required]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        return [
            "MenuView must toggle from recorder state and persist intent before async work"
        ]

    if action.count("await screenRecorder.stop()") != 1:
        return ["MenuView must stop exactly once from the running branch"]
    if action.count("await screenRecorder.start()") != 1:
        return ["MenuView must start exactly once from the stopped branch"]

    return []
