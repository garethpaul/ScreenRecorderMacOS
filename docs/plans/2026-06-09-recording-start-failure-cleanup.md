# Recording Start Failure Cleanup

## Status: Completed

## Context

`ScreenRecorder.start()` starts timer and audio-metering setup before it knows a
capture filter can be built. If no source is selected, or if ScreenCaptureKit
throws while starting, the method could leave audio metering active and the
visible timer in a started state even though recording did not continue.

## Objectives

- Keep successful recording start behavior unchanged.
- Stop audio metering when start exits before recording begins.
- Reset the visible timer on missing-source and thrown-start failures.
- Add deterministic static behavior checks for the cleanup paths.

## Work Completed

- Added `stopAudioMetering()` and `resetTimer()` to the missing-source guard.
- Added the same cleanup calls to the capture-start error handler.
- Extended `scripts/check-capture-source.py --mode behavior` to require both
  cleanup paths.
- Updated README, VISION, and CHANGES notes for start-failure cleanup.

## Verification

- `python3 scripts/check-capture-source.py --mode project`
- `python3 scripts/check-capture-source.py --mode behavior`
- `make lint`
- `make check`
- `make verify`
- `git diff --check`

`xcodebuild` is not installed in this environment, so `make check` reports that
the Xcode build was not run after static verification passes.
