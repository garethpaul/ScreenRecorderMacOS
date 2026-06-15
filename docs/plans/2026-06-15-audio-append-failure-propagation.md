# Audio Append Failure Propagation

Status: Planned

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

## Verification Plan

- Run `make check` from the repository and an external directory with explicit
  timeouts.
- Reject isolated mutations for throwing signature, append result, writer
  error, fallback error, callback catch, guidance, and completed plan.
- Audit the exact diff, generated artifacts, changed-line secrets, staged
  paths, and whitespace before commit.
- Take one bounded exact-head hosted macOS snapshot after push; do not claim
  local Xcode compilation on Linux.

## Scope Boundaries

- Do not change writer configuration, sample formats, readiness guards,
  backpressure behavior, metering, capture selection, timers, persistence, or
  finalization.
- Do not add retries or silently drop failed writer appends.
- Do not claim local Xcode, ScreenCaptureKit, audio-device, or movie playback
  execution on Linux.
- Do not merge or close any pull request without explicit authorization.
