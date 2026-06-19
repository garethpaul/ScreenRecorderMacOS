# Audio Append Failure Propagation

Status: Completed

## Problem

Video sample appends now propagate `AVAssetWriterInput.append` failures through
the capture error handler, but audio appends still discard the boolean result.
An audio writer failure can therefore leave capture appearing healthy while
the output movie is no longer being written reliably.

## Requirements

1. Make `recordAudio` propagate failed sample appends.
2. Use the asset writer error when available and the existing append fallback
   otherwise.
3. Route audio recording errors through `recordingErrorHandler` just like video
   recording errors.
4. Preserve audio metering, sample conversion, readiness/backpressure guards,
   writer startup ownership, video behavior, stop/finalization, and UI state.
5. Add mutation-sensitive static contracts and truthful verification evidence.

## Implementation Units

### 1. Propagate audio append failure

Files:

- `CaptureSample/Record.swift`
- `CaptureSample/CaptureEngine.swift`

Make the audio recorder method throwing, guard the append result, and catch the
error at the ScreenCaptureKit audio callback boundary.

### 2. Protect parity with video

Files:

- `scripts/check-capture-source.py`
- `docs/plans/2026-06-15-audio-append-failure-propagation.md`

Require audio append failure propagation, error-handler routing, method-scoped
ordering, documentation, and completed-plan evidence without weakening video
contracts.

### 3. Document writer integrity

Files:

- `AGENTS.md`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`

Record that failed video or audio sample appends terminate capture through the
shared recording error path.

## Verification Completed

- repository and external-directory `make check` passed with project and
  behavior contracts; Linux truthfully skipped unavailable `xcodebuild`.
- Eight hostile audio append mutations were rejected for the throwing
  signature, append result, writer error, fallback error, callback try/catch,
  guidance, and completed-plan boundaries.
- hostile audio append mutations were rejected.
- generated-artifact, recording-file, and credential-pattern audits passed.
- Hosted macOS compilation will be captured in one bounded exact-head snapshot
  after push without polling.

## Scope Boundaries

- Do not change writer configuration, sample formats, readiness guards,
  backpressure behavior, metering, capture selection, timers, persistence, or
  finalization.
- Do not add retries or silently drop failed writer appends.
- Do not claim local Xcode, ScreenCaptureKit, audio-device, or movie playback
  execution on Linux.
- Do not merge or close any pull request without explicit authorization.
