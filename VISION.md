## Screen Recorder macOS Vision

Screen Recorder macOS is a SwiftUI and ScreenCaptureKit app for recording
display or window content with optional system audio, preview, metering, and
saved recording metadata.

The repository is useful as a focused macOS capture sample that demonstrates
shareable-content discovery, capture filters, SCStream output handling, video
recording, and known recording edge cases.

The goal is to keep screen recording explicit, permission-aware, and reliable
for local demo or sample use.

The current focus is:

Priority:

- MovieRecorder exposes only its video transform at initialization; fixed audio
  and video output settings remain inside startRecording.
- Preserve the ScreenCaptureKit display/window capture flow
- Keep recording permission checks visible
- Store recordings and metadata in documented local locations
- Keep playback tolerant of an empty or invalid recording history
- Avoid hardcoded remote media playback in recording helpers
- Avoid logging saved recording file URLs or metadata
- Keep capture stream continuations tied to explicit start/stop lifecycle
- Release retained capture streams when stop or start failure completes
- Keep the menu bar recording timer reset after recording stops
- Clean up audio metering and timer state when recording start fails
- Propagate writer startup failure before ScreenCaptureKit enters capture
- Stop active capture when a runtime writer start failure rejects the first frame
- Propagate video sample append failure through the existing recording cleanup path
- Video and audio sample append failures propagate through the shared recording cleanup path.
- Remove unfinished movie files when capture setup fails
- Persist recording history only after successful movie finalization and remove
  failed partial outputs
- Keep awaited recording finalization ahead of recorder idle state
- Preserve audio sample forwarding to metering and movie output
- Keep recorder handoff identity explicit and force-unwrap-free
- Keep local Xcode signing team choices out of checked-in project metadata
- Avoid ad hoc stdout debug logging from app Swift sources
- Keep local persistence failures observable without crashing previews
- Keep completed maintenance plans under `docs/plans`
- Keep GitHub Actions running the static `make check` baseline before review
- Keep the unsigned app compiling on a fixed hosted macOS runner
- Maintain README notes for known recording bugs

Next priorities:

- Add setup notes for macOS and Xcode requirements
- Handle sleep, display disconnect, and writer failure cases gracefully
- Add a configuration/viewing pane without hiding recording state

Contribution rules:

- One PR = one focused capture, recording, audio, UI, storage, or documentation change.
- Do not add background recording without explicit user control.
- Include manual verification notes for capture changes.
- Keep `.github/workflows/check.yml` aligned with both the static capture
  baseline and unsigned hosted macOS build.
- Keep recording destinations and permissions documented.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Screen recording can capture sensitive information and audio. The app should
make recording state obvious, keep files local by default, and avoid hidden
capture, upload, or telemetry behavior.

## What We Will Not Merge (For Now)

- Hidden or automatic background recording
- Network upload of recordings
- Permission-bypass behavior
- Ad hoc stdout logging for app state or persistence events
- Storage changes without user-visible documentation

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
