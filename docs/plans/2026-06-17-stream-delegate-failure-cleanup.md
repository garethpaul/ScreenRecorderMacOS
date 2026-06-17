---
title: Route Stream Delegate Failures Through Recording Cleanup
type: fix
date: 2026-06-17
---

# Route Stream Delegate Failures Through Recording Cleanup

Status: In Progress

## Context

Video and audio append failures already use `CaptureEngine.failCapture(_:)` to
cancel the partial movie, finish the engine continuation, clear the retained
stream, and stop capture. `SCStreamDelegate.didStopWithError` instead finishes
a second continuation owned by the stream output, bypassing that cleanup and
leaving recorder state or a partial movie retained after an unexpected stream
stop.

## Requirements

- R1. Route unexpected `SCStreamDelegate` stop errors through the shared
  recording failure handler.
- R2. Cancel partial movie output, finish the engine continuation, clear the
  retained stream, and attempt stream shutdown through the existing cleanup
  path.
- R3. Remove the stream output's duplicate continuation so delegate and sample
  failures cannot diverge again.
- R4. Preserve normal stop behavior and the existing video/audio append-failure
  paths.
- R5. Add mutation-sensitive offline coverage that rejects direct continuation
  completion, swallowed delegate failures, duplicate continuation state, and
  broken cleanup routing.
- R6. Keep Linux validation portable and require the hosted macOS build for
  Apple-framework compilation evidence.

## Scope Boundaries

- Do not redesign recorder ownership, normal finalization, or menu state.
- Do not add dependencies or weaken the existing static and hosted build gates.

## Implementation Units

### U1. Characterize the delegate cleanup bypass

- **Goal:** Define the required delegate-to-handler routing and reject the
  current direct-continuation path.
- **Files:** `scripts/stream_delegate_failure_contract.py`,
  `scripts/test_stream_delegate_failure_contract.py`
- **Verification:** The focused baseline fails before the source fix and each
  hostile mutation is rejected afterward.

### U2. Unify stream failure cleanup

- **Goal:** Route `didStopWithError` through `recordingErrorHandler` and remove
  the stream output continuation that is no longer needed.
- **Files:** `CaptureSample/CaptureEngine.swift`
- **Verification:** Focused contract plus the complete portable repository
  gate.

### U3. Make the boundary durable

- **Goal:** Register the contract, document the lifecycle behavior, and record
  completed evidence.
- **Files:** `scripts/check-capture-source.py`, `Makefile`, `README.md`,
  `CHANGES.md`, `AGENTS.md`,
  `docs/plans/2026-06-17-stream-delegate-failure-cleanup.md`
- **Verification:** Repository and external-directory `make check`, explicit
  mutation checks, and generated-artifact, recording-file, and credential
  audits.

## Verification

- Planned: focused delegate-failure contract and hostile mutations.
- Planned: repository and external-directory `make check` on Linux.
- Planned: hosted macOS build on the exact pushed head.
