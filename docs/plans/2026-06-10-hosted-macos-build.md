# Hosted macOS Build

Status: Completed

## Context

The repository already had dependency-free project and behavior checks, but its
hosted workflow ran only on Linux. Unlike older archived iOS projects, this app
targets macOS 13, uses Swift 5 and system frameworks, has a shared scheme, and
has no third-party package installation step. It can therefore support a real
unsigned build gate on a current hosted macOS image.

## Objectives

- Compile the app on a fixed GitHub-hosted macOS runner.
- Keep signing disabled and account-specific teams out of source control.
- Retain the fast Linux structural and behavior contract.
- Pin all third-party actions to immutable commits.
- Make local verification independent of the caller's working directory.

## Work Completed

- Added an unsigned `xcodebuild` job on the supported `macos-15` runner.
- Kept the Python 3.12 contract job on fixed Ubuntu 24.04.
- Added concurrency cancellation and bounded job timeouts.
- Annotated checkout v6.0.3 and setup-python v6.2.0 immutable commits.
- Anchored Makefile scripts and Xcode execution to the repository root.
- Extended the project checker to fail closed if either hosted gate drifts.

## Verification

- `make check`
- `make -f /path/to/repository/Makefile check` from outside the repository
- Hosted `make build` on `macos-15`
- `git diff --check`
