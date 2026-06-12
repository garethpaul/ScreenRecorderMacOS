# Recorder Handoff Identity

## Status: Completed

## Context

`CaptureEngine.startCapture()` receives a non-optional `MovieRecorder`, assigns
it to the stream output, and immediately force-unwraps that optional property
back into the engine. The unwrap is unnecessary and creates a crash surface in
the capture startup path.

## Priority

The engine and stream output should share the exact recorder supplied by the
caller without optional round trips or force unwraps.

## Requirements

- R1. Assign the caller-provided recorder directly to `CaptureEngine.movie`.
- R2. Assign the same recorder to `CaptureEngineStreamOutput.movie`.
- R3. Reject force-unwrapped recorder handoff paths.
- R4. Preserve recording startup dimensions, cancellation, stream setup, and
  continuation cleanup.
- R5. Protect source, documentation, and completed plan with focused hostile
  mutations and `make check`.

## Scope Boundaries

- Do not redesign `MovieRecorder` ownership or optionality in the stream output.
- Do not change ScreenCaptureKit configuration or recording destinations.
- Do not claim runtime capture verification beyond hosted macOS build evidence.

## Verification Plan

- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- `make build`
- focused recorder-handoff mutations
- `git diff --check`

## Work Completed

- Assigned the caller-provided `MovieRecorder` directly to both the capture
  engine and stream output.
- Removed the optional round trip and force unwrap from capture startup.
- Extended project and behavior checks plus repository guidance to preserve the
  identity handoff.

## Verification

- `python3 scripts/check-capture-source.py --mode project` passed.
- `python3 scripts/check-capture-source.py --mode behavior` passed.
- `make check` passed locally.
- Five focused hostile recorder-handoff mutations were rejected with valid Git
  metadata.
- `git diff --check` passed.
- Local Xcode compilation was unavailable on Linux; exact-head hosted macOS
  `make build` is required before merge.
