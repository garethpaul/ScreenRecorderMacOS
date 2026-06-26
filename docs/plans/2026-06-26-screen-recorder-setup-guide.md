# ScreenRecorder macOS Setup Guide Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Document ScreenRecorder's supported macOS and Xcode setup, Screen Recording permission, automatic-start behavior, capture controls, local output, and verification boundaries from checked-in source.

**Architecture:** Preserve the Swift 5/macOS 13 ScreenCaptureKit app, shared scheme, recording lifecycle, persistence model, Make gates, and hosted workflow. Add fail-closed documentation contracts, then retire only the completed setup roadmap item.

**Tech Stack:** Markdown, Python 3 static contracts, Swift 5, SwiftUI, ScreenCaptureKit, AVFoundation, Core Data, GNU Make, Xcode, GitHub Actions

---

## Status: Completed

### Task 1: Add The Documentation Contract

**Files:**
- Modify: `scripts/check-capture-source.py`
- Test: `scripts/check-capture-source.py`

**Step 1: Write the failing test**

Require the supported baseline, shared scheme, permission path, automatic-start boundary, capture controls, local recording behavior, verification, roadmap, history, and completed-plan evidence.

**Step 2: Run test to verify it fails**

Run: `python3 scripts/check-capture-source.py --mode project`

Expected: FAIL because the generated setup text does not separate these operating boundaries.

### Task 2: Write The Setup Guide

**Files:**
- Modify: `README.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`

**Step 1: Write minimal documentation**

Document Swift 5/macOS 13, the shared `CaptureSample` scheme, local signing, Screen Recording authorization, denied-permission behavior, automatic start/stop intent, display/window and audio controls, local Documents/Core Data output, and portable/native verification.

**Step 2: Run focused contracts**

Run: `python3 scripts/check-capture-source.py --mode project`

Expected: PASS.

### Task 3: Prove Drift Fails Closed

**Files:**
- Test: `scripts/check-capture-source.py`

**Step 1: Apply hostile mutations**

Mutate each setup-guide, roadmap, history, and completed-plan contract in an isolated repository copy.

**Step 2: Verify each mutation fails**

Run the project checker after each mutation.

Expected: every mutation is rejected.

### Task 4: Run The Full Gate

**Files:**
- Verify: `Makefile`

**Step 1: Run repository and external gates**

Run: `/usr/bin/make check`

Run: `cd "$(mktemp -d)" && /usr/bin/make -f /absolute/path/to/Makefile check`

Expected: portable project/behavior/mutation/Make authority gates pass; hosted macOS supplies the unsigned native build.

### Task 5: Commit And Ship

**Files:**
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-26-screen-recorder-setup-guide.md`

**Step 1: Record exact validation**

Add mutation, local gate, hosted build, review, and manual-permission blocker evidence.

**Step 2: Commit**

```bash
git add README.md VISION.md CHANGES.md scripts/check-capture-source.py docs/plans/2026-06-26-screen-recorder-setup-guide.md
git commit -m "docs: document ScreenRecorder setup"
```

## Results

- The focused project checker failed on the absent guide, then passed after the
  source-backed documentation reconciliation.
- All 23 isolated hostile setup-guide mutations were rejected. Two preliminary
  harness runs stopped on an incorrectly represented wrapped Markdown fixture;
  correcting it changed no repository file before the complete passing rerun.
- Checkout and external-directory `/usr/bin/make check` each passed 66 Make
  target/authority cases and 31 existing focused recording mutations; Linux
  truthfully skipped unavailable Xcode.
- Claims were audited against project settings, the shared scheme,
  ScreenCaptureKit permission/configuration code, persisted stop intent,
  Documents/Core Data output, entitlements, and the pinned workflow.
- Live permission, source enumeration, capture, system audio, and playback
  remain an authorized-macOS manual boundary.
