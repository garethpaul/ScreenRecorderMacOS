# Runtime Writer Start Failure

## Status: Planned

## Context

`MovieRecorder.startRecording()` now propagates output URL and writer creation
errors before ScreenCaptureKit starts. The first video frame still calls
`AVAssetWriter.startWriting()` without checking its Boolean result, so a runtime
writer failure can leave capture running even though no movie can be produced.

## Priority

High recording-state integrity. A failed asset-writer transition must terminate
the active capture path instead of presenting a recording that cannot finalize.

## Requirements

- Throw the asset writer's runtime error when `startWriting()` returns `false`,
  with an explicit fallback error when AVFoundation supplies none.
- Forward that error from the screen sample handler to the capture engine.
- Cancel partial movie output, finish the frame stream with the error, and stop
  the retained ScreenCaptureKit stream.
- Preserve successful video/audio forwarding, awaited finalization, and existing
  writer-construction failure behavior.
- Add fail-closed source contracts and keep maintained documentation and
  completed verification evidence aligned.

## Scope Boundaries

- Do not change output location, codec settings, capture permissions, Core Data,
  timer behavior, stream configuration, or supported macOS/Xcode versions.

## Implementation Units

1. Make first-frame writer startup failure a throwing `MovieRecorder` boundary.
2. Route recorder errors through `CaptureEngineStreamOutput` to centralized
   capture cleanup and asynchronous stream shutdown.
3. Extend source contracts and maintained documentation for the runtime failure
   path and completed validation evidence.

## Verification

- focused source and ordering contracts
- repository and external-directory `make check`
- hostile writer-result, error-forwarding, cleanup, documentation, and plan
  mutations
- hosted unsigned macOS build on the exact pull-request head
- generated-artifact, recording-file, credential-pattern, and exact-diff audits

## Risks

- Linux validation is static-only; Swift concurrency and ScreenCaptureKit API
  compatibility require the hosted macOS/Xcode build.
- Runtime permission, device, and AVFoundation failure behavior still requires a
  permission-capable macOS environment for end-to-end validation.
