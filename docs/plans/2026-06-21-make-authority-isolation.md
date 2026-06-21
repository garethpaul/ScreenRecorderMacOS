# Make Authority Isolation

## Status: Completed

## Context

The protected repository root stopped direct `ROOT=/tmp` redirection, but the
repository recipes still accepted caller-controlled shells and tool variables,
and bare tool names could be replaced through `PATH`. Those channels could
replace static contracts or turn the hosted native build into a no-op.

## Requirements

- **R1:** Detect unsupported preload and file-list inputs before repository
  recipes execute, without claiming to undo GNU Make parse-time side effects.
- **R2:** Derive the checkout root safely from the exact Makefile path.
- **R3:** Fix the shell, repository-owned isolated Python launcher, absolute
  Xcode launcher, and bytecode suppression without trusting `PATH`.
- **R4:** Exercise every public target across hostile authority inputs.
- **R5:** Preserve all Swift, project, capture, recording, and signing behavior.

## Implementation

- Hardened repository recipe authority before targets execute.
- Added repository-owned launchers that use `/usr/bin/python3 -I -B` and
  `/usr/bin/xcodebuild`, preventing `PATH` and Python startup-state shadowing.
- Added a macOS-portable `root-test` checkout with spaces, quotes, and
  command-substitution syntax in its path.
- Covered all six public targets across eleven authority modes plus explicit
  file-list/preload rejection and earlier-file detection cases.
- Left Swift source, Xcode project, entitlements, and application behavior
  unchanged.

## Boundary

GNU Make evaluates `MAKEFILES`, `--eval`, and additional `--file` inputs while
it is constructing the build graph. A Makefile cannot prevent code in those
explicit startup inputs from running before or after that Makefile is parsed.
They are therefore unsupported caller-selected programs, not trusted
verification inputs. The repository detects the cases visible when its own
file is parsed and fails before repository recipes execute; CI and documented
usage invoke `make check` without extra startup code.

GNU Make also expands dollar syntax in an absolute `--file` argument before
recording `MAKEFILE_LIST`. Repositories whose path contains `$` therefore use
the documented in-checkout `make check` form; that form is covered with a
literal `$(...)` directory name and does not execute the path text.

## Verification

- `make root-test` passed 66 target/authority cases, one dollar-syntax checkout case, three override rejections, and one earlier-file detection.
- `make check` passed from the repository and through an absolute Makefile path.
- Python and shell syntax checks, `git diff --check`, and repository integrity
  screening passed.
