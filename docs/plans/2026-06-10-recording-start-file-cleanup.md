# Recording Start File Cleanup

## Status: Completed

## Context

`CaptureEngine.startCapture` created the movie writer before configuring the
ScreenCaptureKit stream. If stream setup threw, the continuation and stream
were released but the movie recorder stayed active with an unfinished local
file.

## Objectives

- Cancel the movie writer when capture setup fails.
- Remove the unfinished recording file.
- Avoid persisting metadata for recordings that never started.

## Work Completed

- Added `MovieRecorder.cancelRecording()` to clear writer state and inputs.
- Cancelled the asset writer and removed its output URL on startup failure.
- Called cancellation before finishing the failed capture continuation.
- Extended static behavior checks and maintenance documentation.

## Verification

- `python3 scripts/check-capture-source.py --mode project`
- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- `make verify`
- `git diff --check`
