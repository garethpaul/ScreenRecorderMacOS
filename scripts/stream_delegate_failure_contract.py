#!/usr/bin/env python3


def validation_errors(source):
    output_marker = "private class CaptureEngineStreamOutput"
    if output_marker not in source:
        return ["CaptureEngineStreamOutput must remain defined"]

    engine, output = source.split(output_marker, 1)
    errors = []

    creation = engine.find("let streamOutput = CaptureEngineStreamOutput()")
    handler = engine.find(
        "streamOutput.recordingErrorHandler = { [weak self] error in\n"
        "                self?.failCapture(error)"
    )
    stream = engine.find("stream = SCStream(")
    if min(creation, handler, stream) < 0 or not creation < handler < stream:
        errors.append(
            "CaptureEngine must wire shared failure cleanup before creating the stream"
        )

    if "init(continuation:" in output or "private var continuation:" in output:
        errors.append(
            "CaptureEngineStreamOutput must not retain a duplicate stream continuation"
        )

    method_start = output.find(
        "func stream(_ stream: SCStream, didStopWithError error: Error) {"
    )
    method_end = output.find("\n    }", method_start)
    if method_start < 0 or method_end < 0:
        errors.append("CaptureEngineStreamOutput must handle delegate stop failures")
        return errors

    method = output[method_start:method_end]
    if method.count("recordingErrorHandler?(error)") != 1:
        errors.append(
            "SCStreamDelegate stop failures must reach shared recording cleanup exactly once"
        )
    if "continuation" in method:
        errors.append(
            "SCStreamDelegate stop failures must not finish a private continuation directly"
        )

    return errors
