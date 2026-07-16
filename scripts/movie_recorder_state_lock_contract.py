#!/usr/bin/env python3



# Ported verbatim from ios-app-share's check-baseline.py, the working reference in
# this account: a real scanner handling nested /* */ blocks, string-aware and
# escape-aware. A naive //[^\n]* regex would blank the rest of the line for a
# string containing a URL and fail this contract against correct source.
#
# Every fragment check below matched raw source, so a commented-out lock satisfied
# its own assertion while the code was dead. Verified: wrapping
#
#     stateLock.lock()
#     defer { stateLock.unlock() }
#
# in /* */ on their own lines left `make check` at exit 0 -- all three harness
# targets stayed byte-identical -- while deleting the same two lines IS caught. So
# the contract was live but blind, and commit 25c05ca's serialization fix could be
# removed without any gate noticing.
#
# Note the // -prefix form IS caught here, but only incidentally: it perturbs the
# `defer { stateLock.unlock() }` line that test_movie_recorder_state_lock_contract
# mutates, tripping the harness's own no-op self-check ("mutation did not alter the
# baseline") rather than detecting anything. Own-line delimiters keep the harness
# targets intact and the catch evaporates.
#
# Stripping is applied here rather than repo-wide on purpose: sibling contracts
# depend on comments (screen_recorder_start_stop_contract bounds a method with the
# "/// Stops capturing" doc comment, and check-capture-source asserts a fragment
# that includes "// Unable to start the stream"). This contract's delimiters are all
# code signatures, so stripping is safe here.


def strip_swift_comments(text):
    result = []
    index = 0
    block_depth = 0
    in_string = False
    escaped = False

    while index < len(text):
        character = text[index]
        next_character = text[index + 1] if index + 1 < len(text) else ""

        if block_depth:
            if character == "/" and next_character == "*":
                block_depth += 1
                index += 2
                continue
            if character == "*" and next_character == "/":
                block_depth -= 1
                index += 2
                continue
            if character == "\n":
                result.append(character)
            index += 1
            continue

        if in_string:
            result.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            index += 1
            continue

        if character == '"':
            in_string = True
            result.append(character)
            index += 1
            continue
        if character == "/" and next_character == "/":
            newline = text.find("\n", index + 2)
            if newline == -1:
                break
            result.append("\n")
            index = newline + 1
            continue
        if character == "/" and next_character == "*":
            block_depth = 1
            index += 2
            continue

        result.append(character)
        index += 1

    return "".join(result)

def _method_body(source, signature, next_signature):
    start = source.find(signature)
    if start < 0:
        return None
    end = source.find(next_signature, start)
    if end < 0:
        return None
    return source[start:end]


def validation_errors(source):
    # Assert against live code: a commented-out lock must not satisfy the contract.
    source = strip_swift_comments(source)
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
    # Pin the body as one contiguous construct rather than three independent fragments.
    # Fragment presence cannot distinguish a live lock from a dead one: wrapping the pair
    # in `if false { ... }` keeps all three literals present and uncommented while
    # withStateLock serializes nothing, re-opening the race commit 25c05ca closed.
    # Contiguous-literal form copied from capture_source_reconciliation_contract.py.
    locked_body = (
        "        stateLock.lock()\n"
        "        defer { stateLock.unlock() }\n"
        "        return try operation()\n"
    )
    if helper is None or locked_body not in helper:
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
