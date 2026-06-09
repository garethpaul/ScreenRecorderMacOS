# Capture Stream Release

## Status: Completed

## Context

`CaptureEngine` now stores and clears its active capture continuation, but the
retained `SCStream` reference could survive stop handling or partial start
failure. The capture lifecycle should release the stream reference alongside the
continuation so later starts create a fresh stream.

## Objectives

- Preserve existing ScreenCaptureKit start/stop behavior.
- Clear the retained stream reference when start setup fails.
- Clear the retained stream reference after stop handling finishes.
- Extend static behavior checks to preserve the stream release lifecycle.

## Work Completed

- Cleared `self.stream` in the `startCapture` failure path.
- Cleared `self.stream` in the `stopCapture` defer block alongside the stored
  continuation.
- Extended `scripts/check-capture-source.py` to require stream cleanup on stop
  and start failure.
- Updated README, VISION, and CHANGES notes for the capture stream release
  guard.

## Verification

- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- `git diff --check`

## Xcode Notes

XcodeBuildMCP was not available in this environment, so simulator/macOS app
automation was not run here. The repository `make check` wrapper still runs
`xcodebuild` when that tool is available locally.
