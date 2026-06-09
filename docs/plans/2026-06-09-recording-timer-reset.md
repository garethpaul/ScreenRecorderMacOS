# Recording Timer Reset

## Status: Completed

## Context

The app had a published `ScreenRecorder.timerString`, but the menu bar label and
menu view kept their own timer strings. Those local strings only advanced while
recording was running, so a completed recording could leave stale elapsed time
visible after the recorder stopped.

## Objectives

- Keep one recording timer string on `ScreenRecorder`.
- Reset the visible timer when recording starts or stops.
- Make menu bar and menu view displays read from the centralized timer.
- Keep menu stop/start actions on a single branch so one click cannot
  immediately undo itself.
- Add static checks to prevent stale local timer state from returning.

## Work Completed

- Added `ScreenRecorder.refreshTimer(now:)` and a private `resetTimer()` helper.
- Reset `timerString` before restarting the timer publisher and after
  recording stops.
- Updated the menu bar label to display `screenRecorder.timerString`.
- Updated `MenuView` to bind shared `userStopped` state, use a single
  stop/start branch, and display the recorder timer.
- Extended `scripts/check-capture-source.py` to preserve the centralized timer
  and menu state contract.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check-capture-source.py --mode project`
- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- `git diff --check`

`xcodebuild` is not installed in this environment, so `make check` reports that
the Xcode build was not run after static verification passes.

## Follow-Up Candidates

- Run the menu bar stop/start flow on macOS with Xcode to confirm the visual
  timer reset and overlay state.
- Add graceful handling for sleep, display disconnect, and writer failure cases.
