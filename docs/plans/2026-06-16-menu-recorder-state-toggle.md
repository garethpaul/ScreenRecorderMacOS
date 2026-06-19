# Toggle Recording From Actual Recorder State

Status: Completed

## Context

The menu button chooses start or stop from persisted `userStopped` intent.
After an unexpected capture failure, `ScreenRecorder.isRunning` is false while
`userStopped` remains false, so the next Record click calls the no-op stop path
and requires a second click to restart.

## Requirements

- Choose start or stop from `screenRecorder.isRunning`.
- Persist stop intent before launching asynchronous stop work.
- Clear stop intent before launching asynchronous start work.
- Keep the existing button label and icon driven by recorder state.
- Add mutation-sensitive static coverage for state selection, intent polarity,
  and ordering before each task.
- Keep validation portable on Linux without weakening the hosted macOS build.

## Intended Files

- `CaptureSample/Views/MenuView.swift`
- `scripts/menu_recorder_state_contract.py`
- `scripts/test_menu_recorder_state_contract.py`
- `scripts/check-capture-source.py`
- `Makefile`
- `README.md`
- `CHANGES.md`
- `docs/plans/2026-06-16-menu-recorder-state-toggle.md`

## Verification

- The focused contract passed and six recorder-state mutations were rejected:
  persisted intent choosing the operation, inverted stop intent, late stop
  intent, inverted start intent, late start intent, and duplicate start.
- The existing four persisted-stop autostart mutations remained rejected.
- The repository and external-directory `make check` passed all portable
  project and behavior contracts; `xcodebuild` remained unavailable on Linux
  and was reported without weakening the static or hosted build boundary.
- Exact diff, generated-artifact, recording-file, and credential-pattern audits passed.
- No ScreenCaptureKit permission prompt, live capture, recording, playback, or
  native macOS interaction was exercised locally.
