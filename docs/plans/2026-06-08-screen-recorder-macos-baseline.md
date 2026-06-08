# Screen Recorder macOS Baseline

## Status: Completed

## Context

`ScreenRecorderMacOS` is a SwiftUI and ScreenCaptureKit sample for local screen
recording, preview, audio metering, and saved recording playback. The default
maintenance gate should keep capture crash paths and recording URL handling
visible even when Xcode is unavailable.

## Objectives

- Preserve the display/window capture flow and ScreenCaptureKit project setup.
- Keep capture and playback tolerant of empty selections, unknown stream output
  types, malformed frame metadata, and empty recording history.
- Store completed recording URLs with canonical file URL strings.
- Run static project and behavior checks through `make check`.
- Maintain completed maintenance plans under `docs/plans`.

## Work Completed

- Confirmed `make check` runs project checks, behavior checks, and optional
  Xcode build execution.
- Added canonical `docs/plans` coverage for the current recording baseline.
- Extended project checks to require completed `docs/plans` entries with
  `make check` verification.
- Updated README, VISION, and CHANGES to make the baseline discoverable.

## Verification

- `python3 scripts/check-capture-source.py --mode project`
- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Run the Xcode build on macOS with Xcode installed.
- Add manual verification notes for screen recording permission and playback
  behavior.
