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

- Preserve the ScreenCaptureKit display/window capture flow
- Keep recording permission checks visible
- Store recordings and metadata in documented local locations
- Keep playback tolerant of an empty or invalid recording history
- Avoid hardcoded remote media playback in recording helpers
- Avoid logging saved recording file URLs or metadata
- Keep completed maintenance plans under `docs/plans`
- Maintain README notes for known recording bugs

Next priorities:

- Add setup notes for macOS and Xcode requirements
- Fix timer reset behavior after recording completes
- Handle sleep, display disconnect, and writer failure cases gracefully
- Add a configuration/viewing pane without hiding recording state

Contribution rules:

- One PR = one focused capture, recording, audio, UI, storage, or documentation change.
- Do not add background recording without explicit user control.
- Include manual verification notes for capture changes.
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
- Storage changes without user-visible documentation

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
