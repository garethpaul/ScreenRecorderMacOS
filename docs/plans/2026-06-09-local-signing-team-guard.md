# Local Signing Team Guard

## Status: Completed

## Context

The Xcode project had a concrete `DEVELOPMENT_TEAM` value checked in for both
Debug and Release. This makes the sample carry a machine/account-specific
signing choice and can cause local build confusion for contributors using their
own Apple developer team.

## Objectives

- Keep the sample project buildable with local signing configuration.
- Avoid committing a concrete Apple development team identifier.
- Add a deterministic static check that rejects reintroducing a team ID.

## Work Completed

- Cleared the Debug and Release `DEVELOPMENT_TEAM` settings.
- Extended `scripts/check-capture-source.py --mode project` to require empty
  development-team settings and reject concrete team values.
- Updated README, VISION, and CHANGES notes for the signing metadata guard.

## Verification

- `python3 scripts/check-capture-source.py --mode project`
- `python3 scripts/check-capture-source.py --mode behavior`
- `make lint`
- `make check`
- `make verify`
- `git diff --check`

`xcodebuild` is not installed in this environment, so `make check` reports that
the Xcode build was not run after static verification passes.
