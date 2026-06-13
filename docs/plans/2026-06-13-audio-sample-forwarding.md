# Audio Sample Forwarding

## Status: Planned

## Context

`CaptureEngineStreamOutput` receives ScreenCaptureKit audio sample buffers and
converts them for the live power meter, while `MovieRecorder` configures an
audio writer input and exposes `recordAudio(sampleBuffer:)`. The audio output
branch never calls that recording method, so captured movies can omit system
audio even when audio capture is enabled.

## Priority

Audio metering and movie recording consume different representations of the
same valid sample. The output path should retain metering while forwarding each
accepted audio sample exactly once to the active recorder.

## Objectives

- Preserve invalid-sample rejection before all output handling.
- Keep PCM conversion and power-meter delivery for valid audio samples.
- Forward the same valid audio sample buffer once to `MovieRecorder`.
- Add mutation-sensitive static coverage and synchronized documentation.
- Preserve recording finalization, writer lifecycle, and optional recorder
  handoff contracts.

## Implementation Units

### U1. Forward accepted audio samples

**Files:** `CaptureSample/CaptureEngine.swift`

Call `movie?.recordAudio(sampleBuffer:)` in the audio output branch after PCM
conversion and metering delivery, without changing the screen branch.

### U2. Preserve the audio contract

**Files:** `scripts/check-capture-source.py`, `README.md`, `VISION.md`,
`SECURITY.md`, `CHANGES.md`

Require the audio branch to retain conversion, metering, and one recorder call
in that order. Document the capture boundary and add focused missing-call,
duplicate-call, ordering, documentation, and plan-status mutations.

## Verification

- Focused source-contract check and full `make check` locally and from outside
  the repository root.
- Hosted unsigned Xcode build through canonical push and pull-request events.
- Focused hostile mutations plus Python checker compilation, workflow YAML,
  asset JSON, project XML, secret, artifact, and `git diff --check` audits.

## Scope Boundary

This change does not add microphone capture, alter audio encoding settings,
change ScreenCaptureKit permissions, or claim runtime playback validation in a
permission-capable macOS environment.
