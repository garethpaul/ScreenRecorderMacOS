# Structured App Logging Guard

## Status: Completed

## Context

`ScreenRecorderMacOS` already rejects saved-recording metadata and file-URL
debug prints. Other SwiftUI and persistence paths still used ad hoc
`print(...)` calls for start/stop/change events and Core Data save outcomes.
For a screen recorder, stdout logging should stay intentional because app state,
recording paths, and persistence errors can appear in shared diagnostic logs.

## Objectives

- Remove UI state debug prints from the app flow.
- Preserve diagnostics for Core Data failures through structured logging.
- Add a static guard so active app Swift sources do not reintroduce
  `print(...)` logging.

## Work Completed

- Removed `print(...)` calls from `MenuView` state transitions.
- Replaced Core Data load/save failure prints with `OSLog` error logging and
  removed the successful-save debug print.
- Extended `scripts/check-capture-source.py` to reject active `print(...)`
  calls in `CaptureSample` Swift sources.
- Documented the structured logging guard in README, VISION, and CHANGES.

## Verification

- `python3 scripts/check-capture-source.py --mode project`
- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add subsystem/category names to loggers in a dedicated logging cleanup.
- Review the persistence stack for non-fatal error handling beyond logging.
