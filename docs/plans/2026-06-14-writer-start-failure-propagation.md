# Writer Start Failure Propagation

## Status: Planned

## Context

`MovieRecorder.startRecording()` silently returns when it cannot resolve the
documents directory or create `AVAssetWriter`. `CaptureEngine.startCapture()`
then starts ScreenCaptureKit anyway, so the UI can report an active recording
that has no movie writer and can never produce a saved recording.

## Priority

High recording-state integrity. Capture must not enter a running state unless
the destination writer was created successfully.

## Requirements

- Propagate output-URL and asset-writer creation failures from `MovieRecorder`.
- Finish the capture stream with that error before constructing or starting
  `SCStream`.
- Preserve writer cleanup, successful recorder identity, audio/video forwarding,
  and awaited finalization behavior.
- Add fail-closed source contracts and mutation-sensitive coverage.
- Keep maintained documentation and completed verification evidence aligned.

## Scope Boundaries

- Do not change output location, codec settings, capture permissions, Core Data,
  timer behavior, stream configuration, or supported macOS/Xcode versions.

## Verification

- focused project and behavior source contracts
- repository and external-directory `make check`
- hostile writer-error, ordering, cleanup, documentation, and plan mutations
- hosted unsigned macOS build on canonical push and pull-request events
- generated-artifact, recording-file, credential-pattern, and exact-diff audits
