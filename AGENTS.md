# AGENTS.md

## Repository purpose

`garethpaul/ScreenRecorderMacOS` is a SwiftUI macOS screen-recording sample
built with ScreenCaptureKit.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `ScreenRecorder.xcodeproj` - Xcode project
- `CaptureSample` - repository source or sample assets
- `Configuration` - repository source or sample assets
- `LICENSE` - repository source or sample assets
- `plans` - repository source or sample assets

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Combined verification: `make verify`
- Lint/static checks: `make lint`
- Tests: `make test`
- Build: `make build`
- Local Apple development: `open ScreenRecorder.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Swift (16).
- Preserve legacy Xcode project settings and signing assumptions unless the change is explicitly about modernization.

## Testing guidance

- No dedicated test files were detected; treat `make check` as the minimum baseline.
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-screen-recorder-macos-baseline.md` for the canonical capture and recording safety baseline.
- Video and audio sample append failures propagate through the shared recording cleanup path.
- Keep `MovieRecorder` writer publication, append, cancellation, and finalization
  handoff under its single state lock.
- Unexpected ScreenCaptureKit delegate stops propagate through the shared
  recording cleanup path.
- MovieRecorder exposes only its video transform at initialization; fixed audio
  and video output settings remain inside startRecording.
- Reconcile refreshed displays by `displayID` and windows by `windowID`; object
  instance refreshes must not trigger capture reconfiguration when IDs match.
- See `docs/plans/2026-06-08-local-player-viewer.md` for the local player viewer guard.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
