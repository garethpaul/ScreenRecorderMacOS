# Changes

## 2026-06-15

- Video and audio sample append failures propagate through the shared recording cleanup path.
- Propagated video sample append failure through partial-file cleanup and
  capture-stream shutdown.

## 2026-06-14

- Propagated runtime writer start failure from the first video frame through
  partial-file cleanup and capture-stream shutdown.
- Propagated movie writer startup failures before constructing or starting the
  ScreenCaptureKit stream.

## 2026-06-13

- Added audio sample forwarding from accepted ScreenCaptureKit buffers to the
  movie recorder while preserving live metering.
- Added awaited recording finalization so capture stop returns only after movie
  validation and recording-history persistence complete.

## 2026-06-12

- Required completed `AVAssetWriter` finalization before persisting recording
  history, removed failed partial movies, and cleared recorder input state.
- Added static contracts and a maintenance plan for the recording finalization
  boundary.
- Removed the force unwrap from recorder handoff and added static identity
  coverage for capture startup.

## 2026-06-10

- Cancelled movie writers and removed unfinished recording files when capture
  setup fails before streaming begins.
- Added a least-privilege GitHub Actions check workflow that runs the existing
  static `make check` baseline on all branch pushes, pull requests, and manual
  dispatches with pinned Node 24-compatible actions.
- Added a static project guard requiring the CI workflow and completed CI
  baseline plan to remain checked in.
- Added a real unsigned macOS app build on the fixed `macos-15` hosted runner.
- Made Makefile checks and Xcode execution independent of the caller's directory.
- Replaced the obsolete conditional `CFDictionary` frame-metadata cast with
  validated numeric rectangle fields for current Xcode compatibility.

## 2026-06-09

- Cleared the checked-in Xcode development team and added a static project
  guard so local signing identities are not recommitted.
- Stopped audio metering and reset the visible timer when recording start exits
  before capture begins, with static behavior checks for both failure paths.
- Centralized the menu bar recording timer on `ScreenRecorder` and reset it
  after recording stops, with static validation for stale local timer state.
- Pointed the preview persistence controller at the checked-in `Video` Core
  Data model and replaced persistent-store load crashes with structured logs.
- Cleared retained `SCStream` references on capture stop and start failure, with
  static behavior validation for the release path.
- Stored and cleared the active capture stream continuation so `stopCapture()`
  can finish the engine-level stream lifecycle reliably.
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
