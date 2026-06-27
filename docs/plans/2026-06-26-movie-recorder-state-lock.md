# Movie Recorder State Lock

Status: Completed
Date: 2026-06-26

## Context

ScreenCaptureKit sends video and audio samples to separate dispatch queues.
Those callbacks append through one `MovieRecorder`, while explicit stop and
failure cleanup can concurrently detach, cancel, or finalize the same mutable
`AVAssetWriter` and input properties. The recorder had no synchronization for
that shared state.

## Decision

- Give `MovieRecorder` one private `NSLock` and a defer-unlocked helper.
- Publish the initialized writer and inputs under that lock.
- Serialize video and audio writer-status checks and appends under the same
  lock.
- Atomically detach all writer state before awaited finalization or immediate
  cancellation.
- Keep finalization outside the lock after ownership has been detached.

## Verification

- RED: the new contract rejected the unlocked baseline for all required state
  publication, append, cancellation, and stop-handoff paths.
- GREEN: the focused contract passes and rejects eight isolated mutations.
- Existing behavior and first-video-start contracts remain green.
- Repository and external-root `make check` each pass 66 Make authority cases,
  project and behavior checks, and 39 focused mutations; Linux truthfully
  skips unavailable Xcode.
- Hosted unsigned macOS build, CodeQL, and exact-head review remain release
  gates.

## Manual Verification

On an authorized Mac, record display or window content with system audio,
exercise explicit stop and an induced stream failure, then verify one playable
movie or a cleaned partial file with no crash, hang, or stale recording state.
