# Recorder Settings Contract

Status: Completed

## Problem

`MovieRecorder` accepts and stores caller-supplied audio and video settings,
but `startRecording` shadows both properties with fixed local dictionaries.
The initializer therefore advertises configuration that is silently ignored,
while both production call sites pass empty dictionaries that could not be used
as valid writer output settings.

## Requirements

1. Remove the ignored audio and video settings parameters and stored properties
   from `MovieRecorder`.
2. Keep the existing video transform as the recorder's only initializer input.
3. Update every production call site to use the truthful initializer contract.
4. Preserve the exact fixed PCM audio and H.264 video writer settings,
   recording lifecycle, writer failure propagation, append behavior,
   finalization, persistence, and UI state.
5. Add mutation-sensitive static contracts, synchronized guidance, and
   truthful completion evidence.

## Implementation Units

### 1. Remove the misleading configuration surface

Files:

- `CaptureSample/Record.swift`
- `CaptureSample/CaptureEngine.swift`
- `CaptureSample/ScreenRecorder.swift`

Delete the unused settings state and parameters, retain
`init(videoTransform:)`, and migrate both callers without changing the fixed
writer dictionaries inside `startRecording`.

### 2. Protect the initializer and writer settings

Files:

- `scripts/check-capture-source.py`
- `docs/plans/2026-06-16-recorder-settings-contract.md`

Require the truthful initializer, exact call-site set, absence of the ignored
configuration surface, retained codec fragments, guidance, and completed-plan
evidence.

### 3. Document the fixed-format contract

Files:

- `AGENTS.md`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`

Record that recorder output settings are fixed inside `startRecording` rather
than accepted and silently ignored at initialization.

## Verification Plan

- Capture the pre-change source evidence for the unused properties, shadowing
  local dictionaries, and empty-dictionary call sites.
- Run repository and external-directory `make check`.
- Reject hostile initializer, call-site, codec, guidance, and plan-status
  mutations.
- Audit the exact diff, Swift conflict markers, recording artifacts, generated
  files, modes, whitespace, and credential patterns before shipping.
- Capture one bounded exact-head hosted snapshot after push without polling.

## Scope Boundaries

- Do not make output settings configurable or change their current values.
- Do not change capture permissions, writer startup, sample timing,
  backpressure, append failure handling, stop/finalization, persistence, or UI.
- Do not claim local Xcode, ScreenCaptureKit, audio-device, or movie playback
  execution on Linux.
- PR #12 will be stacked on open PR #11; neither pull request may be merged or
  closed without explicit authorization.

## Verification Completed

- The pre-change source inspection found ignored audio/video settings
  properties, shadowing local dictionaries, and two empty-dictionary call sites.
- repository and external-directory `make check` passed with project and
  behavior contracts; Linux truthfully skipped unavailable `xcodebuild`.
- hostile recorder settings mutations were rejected.
- generated-artifact, recording-file, and credential-pattern audits passed.
- No local Xcode build, ScreenCaptureKit capture, audio device, movie playback,
  credentials, or deployment was exercised.
