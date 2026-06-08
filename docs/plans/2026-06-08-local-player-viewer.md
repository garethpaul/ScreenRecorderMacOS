# Local Player Viewer

## Status: Completed

## Context

`CaptureSample/PlayerViewer.swift` was a tracked source file that initialized
an `AVPlayer` with a hardcoded remote HLS sample URL and started playback during
view initialization. A screen recording sample should not make unsolicited
network playback requests from checked-in helper code.

## Objectives

- Remove the hardcoded remote playback URL.
- Keep the player viewer usable with caller-provided local or explicit URLs.
- Avoid force-unwrapped URL construction in the helper.
- Extend static behavior checks so remote autoplay does not return.

## Work Completed

- Converted `PlayerViewer` to a caller-driven `NSView` wrapper around
  `AVPlayerLayer`.
- Added `load(url:)`, `play()`, and `pause()` methods instead of autoplaying a
  remote stream in `init`.
- Extended `scripts/check-capture-source.py` to reject hardcoded remote player
  URLs and require caller-provided URL loading.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check-capture-source.py --mode project`
- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Remove unused viewer files from the project if they remain unreferenced after
  a full Xcode audit.
- Add macOS manual verification notes for local recording playback once
  `xcodebuild` is available.
