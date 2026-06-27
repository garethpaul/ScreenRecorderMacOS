# Changes

## 2026-06-26 19:57 PDT - P1 - Serialize movie recorder state

### Summary

Protected `MovieRecorder` writer state with one lock so concurrent video,
audio, stop, and failure-cleanup paths cannot race while appending or handing
the writer off for finalization.

### Work completed

- Added a private defer-unlocked state helper around writer publication and
  sample appends.
- Added one atomic writer handoff used by both awaited stop and cancellation.
- Preserved first-video-sample startup and existing append-failure propagation.
- Added a focused source contract with eight hostile synchronization mutations.

### Threads

- Started: none; the bounded recorder ownership defect was handled directly.
- Continued: none.
- Stopped: none.

### Files changed

- `CaptureSample/Record.swift` — serialized mutable asset-writer state.
- `scripts/movie_recorder_state_lock_contract.py` — encoded the lock and atomic
  handoff invariants.
- `scripts/test_movie_recorder_state_lock_contract.py` — added eight hostile
  regression mutations.
- `scripts/check-capture-source.py` and
  `scripts/test_movie_recorder_video_start_contract.py` — reconciled existing
  finalization and first-frame checks with the locked implementation.
- `Makefile`, repository guidance, and the completed plan — registered and
  documented the new boundary.

### Validation

- RED: the focused contract rejected the unlocked baseline across writer
  publication, append, stop, and cancellation ownership.
- GREEN: the focused suite passes with all eight hostile mutations rejected.
- Existing behavior checks and the four-mutation first-video-start suite pass.
- Repository and external-root `make check` each pass 66 Make authority cases,
  project and behavior checks, and 39 focused mutations.
- Python compilation and `git diff --check` pass; Linux truthfully skips
  unavailable Xcode.
- Hosted unsigned macOS build, CodeQL, and exact-head review remain required
  before merge.

### Bugs / findings

- P1: ScreenCaptureKit delivered video and audio on separate queues while stop
  and error cleanup could concurrently clear the same unsynchronized writer
  properties, risking a data race during append or finalization handoff.

### Blockers

- Live capture concurrency still requires an authorized Mac; portable checks
  validate source ownership and mutations rather than ScreenCaptureKit timing.

### Next action

- Run repository and external-root verification, then require hosted build,
  CodeQL, and exact-head review before merging.

## 2026-06-26 03:24 PDT - P2 - Document supported recorder setup

### Summary

Completed the ScreenRecorder macOS/Xcode setup priority with source-backed
guidance for the supported toolchain, Screen Recording authorization,
automatic-start behavior, capture controls, local output, and verification.

### Work completed

- Replaced generic generated setup text with the shared scheme, destination,
  signing, authorization, control, and local-persistence boundaries.
- Documented the inherited camera entitlement versus the active
  ScreenCaptureKit screen/system-audio path.
- Added fail-closed guide, roadmap, history, and completed-plan contracts.

### Threads

- Started: none; the bounded documentation reconciliation was handled directly.
- Continued: none.
- Stopped: none.

### Files changed

- `README.md` — added the operational setup and manual-verification guide.
- `VISION.md` — retired only the completed setup priority.
- `scripts/check-capture-source.py` — added fail-closed guide contracts.
- `docs/plans/2026-06-26-screen-recorder-setup-guide.md` — recorded the plan.
- `CHANGES.md` — recorded this cycle and validation evidence.

### Validation

- Initial project checker — failed on the missing guide, roadmap, and history
  contracts as expected.
- Focused project checker — passed after the guide reconciliation.
- Hostile setup-guide suite — rejected all 23 isolated README, roadmap,
  history, and completed-plan mutations.
- Two preliminary mutation-harness runs stopped before case 7 because the
  wrapped System Settings Markdown phrase did not match the fixture; correcting
  the fixture changed no repository file, and the complete rerun passed.
- Checkout and external-directory `/usr/bin/make check` — each passed 66 Make
  target/authority cases, project and behavior checks, and 31 existing focused
  recording mutations. Linux truthfully skipped unavailable Xcode.
- Source audit — matched every guide claim to the project deployment/signing
  settings, shared scheme, ScreenCaptureKit authorization and configuration,
  persisted stop intent, Documents/Core Data output, and pinned workflow.
- API scan — found no camera API, ScreenCaptureKit microphone-enable, network,
  sharing, or export path in `CaptureSample`.
- `git diff --check` — passed; the change is limited to documentation, its
  static contract, and the completed plan.
- Hosted build, CodeQL, and exact-head review remain pending until the PR head
  is available.

### Bugs / findings

- P2: the previous README did not identify the macOS 13 target, shared scheme,
  Screen Recording denial behavior, automatic recording start, or local output.

### Blockers

- Live authorization, source enumeration, capture, audio, and playback require
  an authorized Mac and cannot be demonstrated by portable static checks.

### Next action

- Require exact-head hosted contract/build and CodeQL before merge, then run
  the same checks on the merge commit.

## 2026-06-25 12:43 PDT - P1 - Reconcile disconnected capture sources

### Summary

Replaced nil-only display/window selection refresh with stable-identifier
reconciliation so disconnected displays and closed windows cannot remain as
stale selected capture sources.

### Work completed

- Added a generic refreshed-selection helper keyed by `displayID` or `windowID`.
- Replaced missing sources with the first current source while retaining the
  refreshed object for unchanged IDs.
- Prevented equivalent refreshed objects from triggering redundant active
  capture configuration updates.
- Added a focused mutation-sensitive source contract and maintenance plan.

### Threads

- Started: none; the focused source lifecycle defect was handled directly.
- Continued: none.
- Stopped: none.

### Files changed

- `CaptureSample/ScreenRecorder.swift` — reconciled refreshed source selection.
- `scripts/capture_source_reconciliation_contract.py` — added source invariant.
- `scripts/test_capture_source_reconciliation_contract.py` — added six hostile
  mutations.
- `Makefile` and `scripts/check-capture-source.py` — registered the new gate.
- `README.md`, `VISION.md`, `AGENTS.md`, and the maintenance plan — documented
  the lifecycle boundary.

### Validation

- Initial focused contract — rejected ten missing reconciliation invariants.
- Focused mutation suite — passed with six hostile mutations rejected.
- Repository and external-directory `make check` — passed 66 Make authority
  cases plus all project, behavior, and mutation contracts; Linux truthfully
  skipped unavailable Xcode.
- Python compilation and `git diff --check` — passed.
- Validation-created Python bytecode was removed; credential, recording-file,
  conflict-marker, and generated-artifact scans were clean.
- Initial exact-head Codex review — clean on
  `7d621210ef28f5b495a600b16e394ea1ea8d7118` with no actionable findings.
- Initial hosted contract and unsigned macOS build jobs — passed for push and
  pull-request events; CodeQL Actions and Python passed while Swift analysis
  remained in progress when this evidence update was prepared.
- Final exact-head review and hosted reruns remain required after this update.

### Bugs / findings

- P1: a disconnected display or closed selected window remained selected after
  ScreenCaptureKit returned a new inventory.

### Blockers

- Live source-disconnect recording requires permission-capable macOS manual
  validation; unsigned hosted compilation cannot exercise ScreenCaptureKit.

### Next action

- Require clean final-head review plus hosted contract, build, and CodeQL gates.

## 2026-06-21

- Isolated repository recipes from caller-controlled roots, shells, tool
  variables, executable shadowing, Python startup state, and bytecode settings,
  with 66 target/authority cases and explicit GNU Make startup-boundary notes.

## 2026-06-19

- Appended the first video sample after starting the asset writer session so
  recordings do not drop the frame that establishes writer timing.
- Guarded recorder start and stop tasks against reentrant async calls before
  capture setup or shutdown awaits can duplicate work.
- Treated ScreenCaptureKit microphone samples like other audio samples and
  wrapped writer finalization state for Swift concurrency checking.

## 2026-06-17

- Unexpected ScreenCaptureKit delegate stops propagate through the shared
  recording cleanup path so partial movie and stream state is released.

## 2026-06-16

- Made the menu recording toggle follow actual recorder state and persist stop
  intent before asynchronous start or stop work.
- MovieRecorder exposes only its video transform at initialization; fixed audio
  and video output settings remain inside startRecording.
- Preserved explicit user-stop intent when an authorized content view appears.

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
