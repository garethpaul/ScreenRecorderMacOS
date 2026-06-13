# Awaited Recording Finalization

## Status: Completed

## Context

`CaptureEngine.stopCapture()` started asynchronous `AVAssetWriter`
finalization through a callback and returned immediately. `ScreenRecorder.stop()`
could therefore publish idle state and reset its timer before the movie URL was
validated and recording history was persisted.

## Priority

Stopping a recording is complete only when the writer has finalized or failed
and the persistence decision is known. Returning earlier creates a race between
UI state, playback history, and the output file lifecycle.

## Objectives

- Expose movie finalization as an async `URL?` result.
- Await `AVAssetWriter.finishWriting` with a checked continuation.
- Resume every absent-writer, failed-finalization, and completed-output path.
- Keep failed partial-file cleanup and completed-status validation.
- Persist metadata before `stopCapture()` returns to `ScreenRecorder.stop()`.
- Add fail-closed source, documentation, and completed-plan contracts.

## Work Completed

- Replaced the escaping completion callback with `async -> URL?`.
- Bridged `finishWriting` through `withCheckedContinuation`.
- Awaited finalization in `CaptureEngine` before creating the Core Data entry.
- Updated behavior checks and project guidance for the awaited boundary.

## Verification

- `python3 scripts/check-capture-source.py --mode behavior`
- `make check` locally and from outside the repository root
- focused async signature, await, continuation, failure, documentation, and
  plan mutations
- Python checker compilation, Swift delimiter, secret, artifact, and
  `git diff --check` audits
- hosted unsigned macOS compilation; runtime capture remains permission-bound

Project and behavior checks plus full `make check` passed locally, with the
documented static-only path because `xcodebuild` is unavailable. All six async
signature, await, checked-continuation, failure-resume, documentation, and plan
mutations were rejected. Python checker compilation and `git diff --check`
passed. That compilation produced an untracked `scripts/__pycache__` artifact;
it is excluded from this commit and left intact under the workspace preservation
policy. Hosted unsigned compilation remains required on the exact PR head.

## Scope Boundary

This orders stop completion behind movie finalization and persistence. It does
not add an XCTest target or exercise ScreenCaptureKit permission prompts,
capture media, playback, or file-system failures in hosted CI.
