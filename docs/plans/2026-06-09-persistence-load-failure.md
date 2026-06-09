# Persistence Load Failure Guard

## Status: Completed

## Context

`PersistenceController` is the app's preview/shared Core Data helper. It pointed
at an `NSPersistentContainer` named `CaptureSample`, but the checked-in data
model is `Video.xcdatamodeld`. It also used `fatalError` when persistent stores
failed to load, which is a poor default for a screen-recording sample because a
local store issue should be logged without hiding the rest of the app lifecycle.

## Objectives

- Use the checked-in `Video` Core Data model.
- Avoid process termination on persistent store load failures.
- Route persistence load failures through structured logging.
- Add static validation so the fatal persistence path does not return.

## Work Completed

- Changed `PersistenceController` to initialize `NSPersistentContainer(name:
  "Video")`.
- Added `OSLog` logging to `PersistenceController`.
- Replaced the store-load `fatalError` with a structured error log.
- Extended `scripts/check-capture-source.py --mode behavior` to require the
  `Video` model and non-crashing persistence load handling.
- Updated README, VISION, and CHANGES.

## Verification

- Negative: `python3 scripts/check-capture-source.py --mode behavior` failed
  before the Swift fix because `PersistenceController` used the wrong model
  name, crashed on load failures, and lacked structured logging.
- `python3 scripts/check-capture-source.py --mode project`
- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- `make verify`
- `git diff --check`

## Xcode Notes

`xcodebuild` was not available in this environment, so macOS build verification
was not run here. The repository `make check` wrapper still runs `xcodebuild`
when that tool is available locally.
