# Recording Log Privacy

## Status: Completed

## Context

`ScreenRecorderMacOS` stores completed recording metadata locally after capture
stops. `CaptureEngine.stopCapture()` still printed the saved `VideoEntry`,
which can include the local recording URL and timing metadata. Those details are
useful in the app state but should not be emitted to logs by default.

## Objectives

- Remove debug logging of saved recording metadata.
- Keep completed recording URL persistence unchanged.
- Extend static behavior checks so recording metadata logging is not
  reintroduced.
- Preserve the existing capture, playback, file URL, project, and docs-plan
  checks.

## Work Completed

- Removed `print(videoEntry)` from `CaptureEngine.stopCapture()`.
- Extended `scripts/check-capture-source.py --mode behavior` to reject saved
  recording metadata logging.
- Ignored Python bytecode artifacts produced by static-checker validation.
- Updated README, VISION, and CHANGES notes for the privacy guard.

## Verification

- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- `make verify`
- `git diff --check`
