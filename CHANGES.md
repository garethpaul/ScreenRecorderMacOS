# Changes

## 2026-06-08

- Added a Makefile verification gate for project/source checks and optional
  Xcode builds when `xcodebuild` is installed.
- Added static tests for ScreenCaptureKit capture contracts.
- Avoided crash-only handling for unknown stream output types and malformed
  frame metadata.
- Made display/window content filters fail closed when no source is selected.
