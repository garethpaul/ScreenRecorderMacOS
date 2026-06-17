#!/usr/bin/env python3
from pathlib import Path

from stream_delegate_failure_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "CaptureSample" / "CaptureEngine.swift").read_text(
    encoding="utf-8"
)

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline stream delegate failure cleanup invalid: {errors}")

delegate_method = (
    "func stream(_ stream: SCStream, didStopWithError error: Error) {\n"
    "        recordingErrorHandler?(error)\n"
    "    }"
)

mutations = {
    "direct continuation completion": baseline.replace(
        delegate_method,
        "func stream(_ stream: SCStream, didStopWithError error: Error) {\n"
        "        continuation?.finish(throwing: error)\n"
        "    }",
        1,
    ),
    "swallowed delegate failure": baseline.replace(
        delegate_method,
        "func stream(_ stream: SCStream, didStopWithError error: Error) {\n"
        "        return\n"
        "    }",
        1,
    ),
    "duplicate continuation state": baseline.replace(
        "private class CaptureEngineStreamOutput: NSObject, SCStreamOutput, SCStreamDelegate {\n"
        "    private let logger = Logger()",
        "private class CaptureEngineStreamOutput: NSObject, SCStreamOutput, SCStreamDelegate {\n"
        "    private let logger = Logger()\n"
        "    private var continuation: AsyncThrowingStream<CapturedFrame, Error>.Continuation?",
        1,
    ),
    "continuation initializer restored": baseline.replace(
        "let streamOutput = CaptureEngineStreamOutput()",
        "let streamOutput = CaptureEngineStreamOutput(continuation: continuation)",
        1,
    ),
    "shared handler wiring removed": baseline.replace(
        "            streamOutput.recordingErrorHandler = { [weak self] error in\n"
        "                self?.failCapture(error)\n"
        "            }\n",
        "",
        1,
    ),
    "duplicate delegate cleanup": baseline.replace(
        delegate_method,
        "func stream(_ stream: SCStream, didStopWithError error: Error) {\n"
        "        recordingErrorHandler?(error)\n"
        "        recordingErrorHandler?(error)\n"
        "    }",
        1,
    ),
}

for description, source in mutations.items():
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(
    "Stream delegate failure cleanup contract passed "
    f"({len(mutations)} mutations rejected)."
)
