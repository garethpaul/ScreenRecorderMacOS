# Screen Recorder macOS CI Baseline

## Status: Completed

## Context

`ScreenRecorderMacOS` has Python-backed static project and behavior checks
behind `make check`, with Xcode builds guarded for macOS hosts. The repository
needs those checks in GitHub Actions so capture, persistence, timer, signing,
and privacy guardrails run before review. Linux CI deliberately cannot prove
ScreenCaptureKit runtime or Xcode build behavior, so the workflow also keeps a
separate unsigned hosted macOS build.

## Objectives

- Run the existing `make check` wrapper in GitHub Actions.
- Keep the hosted job independent of Xcode and ScreenCaptureKit runtime access.
- Use pinned Node 24-compatible actions and least-privilege settings.
- Run an unsigned build on a fixed hosted macOS runner.
- Make the workflow presence part of the static baseline contract.

## Work Completed

- Added `.github/workflows/check.yml` for all branch pushes, pull requests, and
  manual dispatches.
- Pinned checkout and Python setup actions by verified commit SHA.
- Restricted workflow permissions to read-only contents, disabled persisted
  checkout credentials, and bounded both jobs with timeouts.
- Added an unsigned app build on the fixed `macos-15` runner.
- Extended `scripts/check-capture-source.py` to require the CI workflow and
  this completed plan.
- Updated README, VISION, SECURITY, and CHANGES with the CI baseline.

## Verification

- `make check`
- `python3 scripts/check-capture-source.py --mode project`
- `python3 scripts/check-capture-source.py --mode behavior`
- `git diff --check`

## Follow-Up Candidates

- Add ScreenCaptureKit runtime tests when hosted runners can grant capture
  permission without weakening the sample's privacy boundary.
