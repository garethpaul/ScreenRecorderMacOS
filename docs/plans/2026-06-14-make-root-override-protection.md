# Make Root Override Protection

## Status: Planned

## Context

The Makefile derives its repository root from the loaded file and uses that
path for static capture contracts and optional local Xcode builds. GNU Make
command-line variables outrank an ordinary assignment, so `make ROOT=/tmp
check` can redirect those commands away from the checkout.

## Requirements

- **R1:** Prevent command-line and environment values from replacing the
  Makefile-derived repository root.
- **R2:** Keep `PYTHON` and `XCODEBUILD` configurable.
- **R3:** Require the exact protected declaration in the capture checker.
- **R4:** Prove every public Make alias from the checkout and an external
  directory with a hostile `ROOT` argument.
- **R5:** Preserve capture, audio forwarding, recording finalization,
  persistence, signing, workflow, and macOS build contracts.

## Implementation Units

### U1. Protected Root

Give the repository-derived root override precedence without changing recipes,
tool selection, or the conditional local Xcode build.

### U2. Capture Contract

Extend `scripts/check-capture-source.py` to reject weakened, duplicate,
displaced, or caller-controlled root declarations and incomplete evidence.

### U3. Verification

Run project and behavior contracts, all Make aliases, external hostile
execution, Python 3.12 validation, mutations, and integrity screening.

## Scope Boundary

- Do not modify Swift, entitlements, project settings, or recording behavior.
- Do not change hosted actions, macOS runner, Xcode build, or signing policy.
- Do not add recordings, DerivedData, caches, or credentials.

## Verification

- `python3 scripts/check-capture-source.py --mode project`
- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- external `make ROOT=/tmp check`
- root-declaration, checker, plan-status, README-index, and evidence mutations
- Python syntax, workflow YAML, protected-file, secret, artifact, and
  `git diff --check` gates
