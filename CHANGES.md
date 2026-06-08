# Changes

## 2026-06-08

- Made recording file URL creation use `FileManager` URL APIs instead of
  force-unwrapped path strings.
- Saved completed recording URLs with `absoluteString` and made the last
  recording player tolerate an empty or invalid history.
- Extended the source checker to protect the recording URL storage and playback
  guardrails.
- Added a Makefile verification gate for project/source checks and optional
  Xcode builds when `xcodebuild` is installed.
- Added static tests for ScreenCaptureKit capture contracts.
- Avoided crash-only handling for unknown stream output types and malformed
  frame metadata.
- Made display/window content filters fail closed when no source is selected.
