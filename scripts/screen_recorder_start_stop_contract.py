#!/usr/bin/env python3


def _method_body(source, signature, next_marker):
    start = source.find(signature)
    if start < 0:
        return None
    end = source.find(next_marker, start)
    if end < 0:
        return None
    return source[start:end]


def validation_errors(source):
    errors = []

    if "private var isStartTaskActive = false" not in source:
        errors.append("ScreenRecorder must track an active start task")
    if "private var isStopTaskActive = false" not in source:
        errors.append("ScreenRecorder must track an active stop task")

    start_body = _method_body(source, "func start() async {", "\n    /// Stops capturing")
    if start_body is None:
        errors.append("ScreenRecorder.start must remain async")
    else:
        required_start_order = (
            "guard !isRunning, !isStartTaskActive, !isStopTaskActive else { return }",
            "isStartTaskActive = true",
            "defer { isStartTaskActive = false }",
            "if !isSetup {",
            "await monitorAvailableContent()",
            "isRunning = true",
            "for try await frame in captureEngine.startCapture",
        )
        positions = [start_body.find(fragment) for fragment in required_start_order]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            errors.append(
                "ScreenRecorder.start must guard reentrant start/stop work before its first await"
            )
        if start_body.count("await monitorAvailableContent()") != 1:
            errors.append("ScreenRecorder.start must monitor available content exactly once")

    stop_body = _method_body(source, "func stop() async {", "\n\n    func refreshTimer")
    if stop_body is None:
        errors.append("ScreenRecorder.stop must remain async")
    else:
        required_stop_order = (
            "guard isRunning, !isStopTaskActive else { return }",
            "isStopTaskActive = true",
            "defer { isStopTaskActive = false }",
            "await captureEngine.stopCapture()",
            "isRunning = false",
        )
        positions = [stop_body.find(fragment) for fragment in required_stop_order]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            errors.append(
                "ScreenRecorder.stop must reject duplicate stop work before awaiting capture shutdown"
            )
        if stop_body.count("await captureEngine.stopCapture()") != 1:
            errors.append("ScreenRecorder.stop must stop capture exactly once")

    return errors
