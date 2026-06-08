# Capture Safety Gate

## Problem

The macOS sample had no repo-local verification command and the capture path
contained fatal crash paths for unknown ScreenCaptureKit stream output types,
unexpected frame metadata shapes, and missing display/window selections.

## TDD Evidence

1. Added `scripts/check-capture-source.py` and a Makefile `test` target.
2. Ran `make test` before implementation changes and confirmed it failed on
   the fatal capture paths.
3. Replaced the fatal paths with logged or nil-return handling and reran the
   full verification gate.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `git diff --check`
