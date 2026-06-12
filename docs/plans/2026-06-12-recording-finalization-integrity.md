# Recording Finalization Integrity

## Status: Completed

## Context

`MovieRecorder.stopRecording` currently invokes its completion with the output
URL after `AVAssetWriter.finishWriting`, regardless of whether the writer
actually completed. `CaptureEngine.stopCapture` treats every callback URL as a
valid movie and persists a `VideoEntry`, which can leave failed or partial
files in Documents and invalid entries in recording history.

## Priority

Only a successfully finalized movie should become durable recording metadata.
Failed finalization must clean up the partial local file without exposing its
URL as a completed recording.

## Requirements

- R1. Make recording finalization invoke its completion exactly once and report
  the output URL only when the asset writer reaches `.completed`; report no URL
  when no writer is active or finalization fails.
- R2. Clear the recorder's writer and input references when stopping so stale
  state cannot leak into a later recording.
- R3. Remove the partial output file when finalization does not complete.
- R4. Skip `VideoEntry` creation and persistence when finalization reports no
  completed URL.
- R5. Preserve the successful recording path, including `absoluteString`
  metadata storage and existing start/end timestamps.
- R6. Protect the behavior with source contracts, focused hostile mutations,
  repository documentation, and the full `make check` gate.
- R7. Do not log failed recording file URLs or other captured-content metadata.

## Scope Boundaries

- Do not change recording destinations, codecs, capture filters, or permission
  behavior.
- Do not redesign Core Data storage or add network reporting.
- Do not claim interactive recording verification without running the app on a
  compatible macOS host with Screen Recording permission.

## Implementation Units

### Recorder finalization contract

**Files:** `CaptureSample/Record.swift`

- Return an optional completed URL from the stop callback.
- Complete the callback with no URL when there is no active writer.
- Clear writer and input references before asynchronous finalization returns.
- Check the terminal writer status and delete the output on failure.

### Metadata persistence boundary

**Files:** `CaptureSample/CaptureEngine.swift`

- Require a non-nil completed URL before creating a `VideoEntry`.
- Preserve the existing completed-recording metadata fields and save path.

### Regression contracts and maintenance record

**Files:** `scripts/check-capture-source.py`, `README.md`, `SECURITY.md`,
`VISION.md`, `CHANGES.md`, `docs/plans/2026-06-12-recording-finalization-integrity.md`

- Require the optional completion contract, terminal success check, failure
  cleanup, state cleanup, and guarded persistence.
- Document the completed-only recording history boundary and validation limits.

## Verification Plan

- `python3 scripts/check-capture-source.py --mode project`
- `python3 scripts/check-capture-source.py --mode behavior`
- `make check`
- `make build`
- focused finalization and persistence hostile mutations
- `git diff --check`
- exact-head hosted macOS unsigned build before merge

## Work Completed

- Made `MovieRecorder.stopRecording` complete exactly once with an optional
  URL, clearing recorder state before handling either active or absent writers.
- Required terminal `.completed` writer status before returning a movie URL and
  removed the partial output for every other terminal result.
- Guarded `VideoEntry` creation on a completed recording URL while preserving
  existing timestamps and `absoluteString` persistence.
- Extended source contracts and maintenance guidance for the finalization
  boundary.

## Verification

- `python3 scripts/check-capture-source.py --mode behavior` passed.
- Eight focused hostile finalization and persistence mutations were rejected.
- `python3 -m py_compile scripts/check-capture-source.py` passed.
- `make check` passed with project and behavior checks; local Xcode compilation
  was unavailable on Linux and was explicitly skipped by the Makefile.
- An external-directory invocation of the repository Makefile passed from
  `/tmp`, proving the gate is independent of the caller's working directory.
- Plan-aware correctness, maintainability, project-standards, testing,
  reliability, and Swift lifecycle review found no actionable issues.
- `git diff --check` passed.

## Remaining Risks

- Static contracts and compilation do not exercise disk-full, encoder, sleep,
  or display-disconnect failures at runtime.
- Interactive capture still requires a compatible macOS host, Screen Recording
  permission, and manual inspection of recording history and partial files.
