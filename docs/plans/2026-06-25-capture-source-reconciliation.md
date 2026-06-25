# Capture Source Reconciliation

Status: Completed

## Context

`refreshAvailableContent()` only selected the first display or window when the
current selection was `nil`. If a selected display disconnected or a selected
window closed, the model retained an object that was no longer present in the
latest ScreenCaptureKit inventory. The picker could have no represented
selection and later capture configuration could continue from stale source
state.

## Priority

P1 capture-source correctness. A disappearing source must move selection to an
available source instead of retaining a disconnected display or closed window.

## Requirements

- Match refreshed displays by `displayID` and windows by `windowID`.
- Replace a missing selection with the first currently available source.
- Refresh the selected object when the stable identifier remains available.
- Avoid reconfiguring active capture when only the object instance refreshes
  and its stable identifier is unchanged.
- Preserve existing capture type, permission, recording, audio, timer,
  persistence, and failure-cleanup behavior.
- Add mutation-sensitive dependency-free contracts.

## Verification

- Prove the pre-fix source fails the focused reconciliation contract.
- Reject mutations for both identifier guards, both source refreshes, first
  source fallback, and restored nil-only behavior.
- Run root and external-directory `make check`.
- Require hosted unsigned macOS compilation and exact-head Codex review before
  merge.

## Risks

- Permission-capable live display disconnect and window-close behavior cannot
  run on this Linux host or in an unsigned hosted build.
- ScreenCaptureKit may return refreshed object instances for an unchanged
  source; stable-ID guards must prevent unnecessary stream updates.

## Verification Completed

- The pre-fix source failed the focused contract with ten missing invariants.
- six capture-source mutations were rejected for display/window identity guards,
  display/window reconciliation, first-source fallback, and nil-only behavior.
- repository and external-directory `make check` passed all portable project,
  behavior, mutation, and Make-authority gates; Linux truthfully skipped Xcode.
- hosted unsigned macOS compilation passed before merge.
- Exact-head review evidence is recorded in `CHANGES.md` before merge.
