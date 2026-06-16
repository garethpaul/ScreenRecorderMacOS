# Preserve Explicit Stop Intent On App Appearance

Status: Planned

## Context

`ContentView` persists the user's explicit stop choice in `userStopped`, but
its appearance task starts screen capture whenever permission is available.
Relaunching or rebuilding the view can therefore resume capture despite the
persisted stop intent.

## Objectives

- Keep permission validation as the outer prerequisite for capture.
- Start capture on appearance only when `userStopped` is false.
- Preserve the existing unauthorized overlay and input-disable behavior.
- Add mutation-sensitive static coverage for guard presence, polarity, and
  ordering before `screenRecorder.start()`.

## Scope Boundaries

- Do not change manual start/stop controls, timer behavior, recording output,
  capture configuration, permissions, entitlements, or persistence schema.
- Do not add generated recordings, build output, credentials, or dependencies.

## Implementation

1. Guard the authorized appearance auto-start with persisted `userStopped`.
2. Extend the source checker through a focused reusable validator.
3. Add hostile mutations for missing, inverted, and late guards.
4. Synchronize repository guidance and record completed verification.

## Verification

- Prove the pre-fix source fails the new focused contract.
- Run the focused mutation suite.
- Run repository-root and external-directory `make check`.
- Record the Linux `xcodebuild` limitation without weakening static checks.
- Audit the exact diff, generated artifacts, recording files, credential
  patterns, conflict markers, binaries, modes, and large files.
