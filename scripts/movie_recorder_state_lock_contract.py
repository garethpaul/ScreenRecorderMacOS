#!/usr/bin/env python3


def _method_body(source, signature, next_signature):
    start = source.find(signature)
    if start < 0:
        return None
    end = source.find(next_signature, start)
    if end < 0:
        return None
    return source[start:end]


def validation_errors(source):
    errors = []

    if "private let stateLock = NSLock()" not in source:
        errors.append("MovieRecorder must own a private state lock")
    if "private var isRecording = false" not in source:
        errors.append("MovieRecorder recording state must not expose an unlocked getter")

    helper = _method_body(
        source,
        "private func withStateLock<Result>",
        "    private func documentDirectory()",
    )
    if helper is None or not all(
        fragment in helper
        for fragment in (
            "stateLock.lock()",
            "defer { stateLock.unlock() }",
            "return try operation()",
        )
    ):
        errors.append("MovieRecorder must provide a defer-unlocked state helper")

    method_contracts = (
        (
            "func startRecording(height: Int, width: Int) throws {",
            "    func stopRecording() async -> URL?",
            "withStateLock {",
            "MovieRecorder.startRecording must publish writer state under the state lock",
        ),
        (
            "func cancelRecording() {",
            "    func recordVideo(sampleBuffer: CMSampleBuffer) throws {",
            "takeAssetWriter()",
            "MovieRecorder.cancelRecording must detach writer state under the state lock",
        ),
        (
            "func recordVideo(sampleBuffer: CMSampleBuffer) throws {",
            "    func recordAudio(sampleBuffer: CMSampleBuffer) throws {",
            "try withStateLock {",
            "MovieRecorder.recordVideo must serialize writer access under the state lock",
        ),
    )
    for signature, next_signature, lock_call, message in method_contracts:
        body = _method_body(source, signature, next_signature)
        if body is None or lock_call not in body:
            errors.append(message)

    audio_start = source.find("func recordAudio(sampleBuffer: CMSampleBuffer) throws {")
    audio_body = source[audio_start:] if audio_start >= 0 else None
    if audio_body is None or "try withStateLock {" not in audio_body:
        errors.append("MovieRecorder.recordAudio must serialize writer access under the state lock")

    stop_body = _method_body(
        source,
        "func stopRecording() async -> URL? {",
        "    func cancelRecording() {",
    )
    if stop_body is None or not all(
        fragment in stop_body
        for fragment in (
            "let assetWriter = takeAssetWriter()",
            "private func takeAssetWriter() -> AVAssetWriter?",
        )
    ):
        errors.append("MovieRecorder.stopRecording must atomically detach writer state before awaiting finalization")

    take_writer = _method_body(
        source,
        "private func takeAssetWriter() -> AVAssetWriter? {",
        "    func cancelRecording() {",
    )
    if take_writer is None or not all(
        fragment in take_writer
        for fragment in (
            "withStateLock {",
            "let assetWriter = self.assetWriter",
            "isRecording = false",
            "self.assetWriter = nil",
            "assetWriterAudioInput = nil",
            "assetWriterVideoInput = nil",
            "return assetWriter",
        )
    ):
        errors.append("MovieRecorder must clear all writer state atomically")

    return errors
