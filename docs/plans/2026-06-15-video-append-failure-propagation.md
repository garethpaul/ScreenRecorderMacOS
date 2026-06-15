# Video Append Failure Propagation

## Status: Completed

## Context

`MovieRecorder.recordVideo()` propagates `AVAssetWriter.startWriting()` failure,
but it ignores the Boolean result of `AVAssetWriterInput.append(_:)`. A writer
that stops accepting video samples can therefore leave capture running until a
later stop, producing an incomplete or failed recording without using the
existing recording-error cleanup path.

## Priority

High recording-integrity resilience. A rejected video sample should fail the
capture immediately and remove the partial movie through the established
runtime writer failure boundary.

## Requirements

- Treat a `false` video input append result as a recording failure.
- Prefer the writer's concrete error and provide a stable fallback error.
- Propagate the error through `recordVideo()` to the existing
  `recordingErrorHandler` and `failCapture(_:)` cleanup path.
- Preserve readiness checks, audio forwarding, writer startup, finalization,
  persistence, and cancellation semantics.
- Add fail-closed static and mutation-sensitive contracts.

## Scope Boundaries

- Do not change audio append behavior, capture configuration, project settings,
  dependencies, persistence schema, or UI behavior.
- Do not claim permission-capable runtime recording validation from Linux or
  unsigned hosted builds.
- Do not merge or close stacked pull requests without explicit authorization.

## Implementation Units

1. Add a fallback append-failure error and throw when the ready video input
   rejects a sample.
2. Extend the source checker to protect append-result handling and the existing
   error handoff.
3. Update maintained documentation and completed verification evidence.

## Verification

- focused source-contract validation
- repository and external-directory `make check`
- hostile append-result, fallback-error, error-handoff, documentation, and
  completed-plan mutations
- workflow YAML, plist, scheme XML, Python artifact, recording artifact,
  credential-pattern, and exact-diff audits

## Verification Results

- Focused behavior and project source-contract validation passed.
- The repository and external-directory `make check` passed; Linux truthfully
  used the documented static-only path because `xcodebuild` is unavailable.
- Six hostile video append mutations were rejected across fallback error,
  append-result handling, error handoff, documentation, plan status, and
  completed evidence.
- The generated-artifact, recording-file, and credential-pattern audits passed,
  along with workflow YAML, entitlements plist, shared scheme XML,
  conflict-marker, and exact-diff checks.

## Remaining Risks

- Permission-capable ScreenCaptureKit and AVAssetWriter append failure behavior
  still requires end-to-end macOS runtime validation.
- Hosted unsigned compilation proves source compatibility but does not grant
  screen-recording permission or exercise a live movie writer failure.
