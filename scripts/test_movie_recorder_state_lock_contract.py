#!/usr/bin/env python3
from pathlib import Path

from movie_recorder_state_lock_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
baseline = (ROOT / "CaptureSample" / "Record.swift").read_text(encoding="utf-8")

errors = validation_errors(baseline)
if errors:
    raise AssertionError(f"baseline movie recorder state-lock contract invalid: {errors}")

mutations = {
    "state lock removed": baseline.replace("    private let stateLock = NSLock()\n", "", 1),
    "recording state getter exposed": baseline.replace(
        "    private var isRecording = false\n",
        "    private(set) var isRecording = false\n",
        1,
    ),
    "unlock defer removed": baseline.replace("        defer { stateLock.unlock() }\n", "", 1),
    "start publication unlocked": baseline.replace("        withStateLock {\n", "        do {\n", 1),
    "stop detachment bypassed": baseline.replace(
        "        let assetWriter = takeAssetWriter()\n",
        "        let assetWriter = self.assetWriter\n",
        1,
    ),
    "cancel detachment unlocked": baseline.replace(
        "        guard let assetWriter = takeAssetWriter() else {",
        "        guard let assetWriter = self.assetWriter else {",
        1,
    ),
    "video append unlocked": baseline.replace(
        "    func recordVideo(sampleBuffer: CMSampleBuffer) throws {\n        try withStateLock {",
        "    func recordVideo(sampleBuffer: CMSampleBuffer) throws {\n        do {",
        1,
    ),
    "audio append unlocked": baseline.replace(
        "    func recordAudio(sampleBuffer: CMSampleBuffer) throws {\n        try withStateLock {",
        "    func recordAudio(sampleBuffer: CMSampleBuffer) throws {\n        do {",
        1,
    ),
}

for description, source in mutations.items():
    if source == baseline:
        raise AssertionError(f"{description} mutation did not alter the baseline")
    if not validation_errors(source):
        raise AssertionError(f"{description} mutation was accepted")

print(
    "Movie recorder state-lock contract passed "
    f"({len(mutations)} mutations rejected)."
)
