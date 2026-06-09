# Changes

## 2026-06-09

- Removed ad hoc Swift `print(...)` debug logging from menu state transitions
  and Core Data save paths.
- Routed Core Data persistence failures through structured `OSLog` logging and
  extended static checks to reject active `print(...)` app logging.

## 2026-06-08

- Removed saved recording metadata debug logging and added static validation to
  keep recording file URLs out of logs.
- Ignored Python bytecode artifacts produced while validating the static
  source checker.
- Removed hardcoded remote playback from `PlayerViewer` and extended static
  checks to require caller-provided recording URLs.
- Added `make check` as the shared repository verification alias.
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
- Added canonical `docs/plans` coverage and made project checks require
  completed plans.
