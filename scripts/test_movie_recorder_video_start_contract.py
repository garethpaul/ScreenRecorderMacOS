#!/usr/bin/env python3
from pathlib import Path

from movie_recorder_video_start_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "CaptureSample" / "Record.swift").read_text(encoding="utf-8")

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline movie recorder video-start contract invalid: {errors}")

first_append_guard = (
    "            guard assetWriter.status == .writing,\n"
    "                let input = assetWriterVideoInput,\n"
    "                input.isReadyForMoreMediaData else {\n"
    "                    return\n"
    "            }\n\n"
    "            guard input.append(sampleBuffer) else {\n"
    "                throw assetWriter.error ?? MovieRecorderError.assetWriterAppendFailed\n"
    "            }\n"
)

mutations = {
    "first sample hidden behind else-if": baseline.replace(
        "            guard assetWriter.status == .writing,",
        "            } else if assetWriter.status == .writing {\n"
        "                guard",
        1,
    ),
    "first sample append removed": baseline.replace(first_append_guard, "", 1),
    "append failure swallowed": baseline.replace(
        "guard input.append(sampleBuffer) else {\n"
        "                throw assetWriter.error ?? MovieRecorderError.assetWriterAppendFailed\n"
        "            }",
        "_ = input.append(sampleBuffer)",
        1,
    ),
    "append duplicated": baseline.replace(
        "guard input.append(sampleBuffer) else {",
        "_ = input.append(sampleBuffer)\n            guard input.append(sampleBuffer) else {",
        1,
    ),
}

for description, source in mutations.items():
    if source == baseline:
        raise AssertionError(f"{description} mutation did not alter the baseline")
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(
    "Movie recorder video-start contract passed "
    f"({len(mutations)} mutations rejected)."
)
