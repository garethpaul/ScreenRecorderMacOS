# Capture Continuation Lifecycle

## Status: Completed

## Context

`CaptureEngine` stores a stream continuation property that `stopCapture()`
finishes, but `startCapture()` did not assign that property. The stream output
helper had its own continuation, yet the engine-level stop path could not
finish or clear the active continuation reliably.

## Objectives

- Keep existing ScreenCaptureKit start/stop behavior intact.
- Store the active `AsyncThrowingStream` continuation when capture starts.
- Clear the stored continuation after stop or start failure.
- Extend static behavior checks to preserve the continuation lifecycle.

## Work Completed

- Assigned `self.continuation` inside `startCapture()`.
- Cleared the stored continuation when stream setup fails.
- Added a `defer` in `stopCapture()` to clear the stored continuation after
  stop handling.
- Extended `scripts/check-capture-source.py` to validate the lifecycle.

## Verification

- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- `make verify`
- `git diff --check`

## Xcode Notes

`xcodebuild` was not available in this environment, so macOS build verification
was not run here. The repository `make check` wrapper still runs `xcodebuild`
when that tool is available locally.
