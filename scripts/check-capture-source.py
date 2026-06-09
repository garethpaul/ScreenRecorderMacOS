#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-screen-recorder-macos-baseline.md"
TIMER_RESET_PLAN = DOCS_PLANS / "2026-06-09-recording-timer-reset.md"


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require_paths():
    missing = []
    for relative_path in (
        "ScreenRecorder.xcodeproj/project.pbxproj",
        "ScreenRecorder.xcodeproj/xcshareddata/xcschemes/CaptureSample.xcscheme",
        "CaptureSample/CaptureEngine.swift",
        "CaptureSample/ScreenRecorder.swift",
        "CaptureSample/CaptureSampleApp.swift",
        "CaptureSample/ContentView.swift",
        "CaptureSample/Record.swift",
        "CaptureSample/PlayerViewer.swift",
        "CaptureSample/PersistenceController.swift",
        "CaptureSample/Views/MenuView.swift",
        "CaptureSample/CaptureSample.entitlements",
    ):
        if not (ROOT / relative_path).exists():
            missing.append(f"missing required project file: {relative_path}")
    return missing


def docs_plan_checks():
    errors = []
    if not CANONICAL_PLAN.exists():
        errors.append("docs/plans/2026-06-08-screen-recorder-macos-baseline.md is missing")
    if not TIMER_RESET_PLAN.exists():
        errors.append("docs/plans/2026-06-09-recording-timer-reset.md is missing")

    plans = sorted(DOCS_PLANS.glob("*.md")) if DOCS_PLANS.exists() else []
    if not plans:
        errors.append("docs/plans must contain at least one completed plan")

    for plan_path in plans:
        plan = plan_path.read_text(encoding="utf-8")
        if "Status: Completed" not in plan or "make check" not in plan:
            errors.append(f"{plan_path.relative_to(ROOT)} must record completed status and make check verification")

    return errors


def project_checks():
    errors = docs_plan_checks() + require_paths()
    if errors:
        return errors

    project = read_text("ScreenRecorder.xcodeproj/project.pbxproj")
    required_project_fragments = (
        "ScreenCaptureKit.framework",
        "CODE_SIGN_ENTITLEMENTS = CaptureSample/CaptureSample.entitlements;",
        "MACOSX_DEPLOYMENT_TARGET = 13;",
        'PRODUCT_BUNDLE_IDENTIFIER = "com.example.apple-samplecode.CaptureSample${SAMPLE_CODE_DISAMBIGUATOR}";',
    )
    for fragment in required_project_fragments:
        if fragment not in project:
            errors.append(f"project is missing expected setting: {fragment}")

    if 'DEVELOPMENT_TEAM = "";' not in project:
        errors.append("project must leave DEVELOPMENT_TEAM empty for local sample signing")
    for line_number, line in enumerate(project.splitlines(), 1):
        if "DEVELOPMENT_TEAM =" in line and 'DEVELOPMENT_TEAM = "";' not in line:
            errors.append(f"project.pbxproj:{line_number} must not commit a concrete DEVELOPMENT_TEAM")

    entitlements = read_text("CaptureSample/CaptureSample.entitlements")
    if "<plist version=\"1.0\">" not in entitlements:
        errors.append("entitlements file is not an XML plist")

    return errors


def behavior_checks():
    errors = require_paths()
    if errors:
        return errors

    capture_engine = read_text("CaptureSample/CaptureEngine.swift")
    screen_recorder = read_text("CaptureSample/ScreenRecorder.swift")
    capture_app = read_text("CaptureSample/CaptureSampleApp.swift")
    content_view = read_text("CaptureSample/ContentView.swift")
    record = read_text("CaptureSample/Record.swift")
    player_viewer = read_text("CaptureSample/PlayerViewer.swift")
    persistence_controller = read_text("CaptureSample/PersistenceController.swift")
    menu_view = read_text("CaptureSample/Views/MenuView.swift")

    if "import ScreenCaptureKit" not in capture_engine:
        errors.append("CaptureEngine.swift must import ScreenCaptureKit")
    if "func startCapture(" not in capture_engine or "func stopCapture()" not in capture_engine:
        errors.append("CaptureEngine must expose start and stop capture operations")
    if "AsyncThrowingStream<CapturedFrame, Error> { continuation in\n            self.continuation = continuation" not in capture_engine:
        errors.append("CaptureEngine.startCapture must store its stream continuation for stopCapture")
    if "defer {\n            self.continuation = nil\n            self.stream = nil\n        }" not in capture_engine:
        errors.append("CaptureEngine.stopCapture must clear its stored stream continuation and stream reference")
    if capture_engine.count("self.stream = nil") < 2:
        errors.append("CaptureEngine must clear retained stream references on stop and start failure")
    if "fatalError(\"Encountered unknown stream output type:" in capture_engine:
        errors.append("CaptureEngine must not crash on unknown SCStream output types")
    if "as! CFDictionary" in capture_engine:
        errors.append("CaptureEngine must not force-cast frame metadata dictionaries")
    if "fatalError(\"No display selected." in screen_recorder:
        errors.append("ScreenRecorder display selection should fail before building a content filter")
    if "fatalError(\"No window selected." in screen_recorder:
        errors.append("ScreenRecorder window selection should fail before building a content filter")
    if "videos[0]" in content_view:
        errors.append("ContentView must not assume a saved recording exists")
    if "URL(string: videos" in content_view or "url!)!" in content_view:
        errors.append("ContentView must not force unwrap saved recording URLs")
    if "private var latestRecordingURL: URL?" not in content_view:
        errors.append("ContentView must centralize optional latest-recording URL parsing")
    if "if let latestRecordingURL = latestRecordingURL" not in content_view:
        errors.append("ContentView must guard playback on a valid saved recording URL")
    if "URL(string: path)" in record or "filePath!" in record:
        errors.append("MovieRecorder must create file URLs without force-unwrapping path strings")
    if "FileManager.default.urls(for: .documentDirectory" not in record:
        errors.append("MovieRecorder must resolve the document directory with FileManager URL APIs")
    if "url.description" in capture_engine:
        errors.append("CaptureEngine must persist recording URLs with absoluteString, not description")
    if "videoEntry.url = url.absoluteString" not in capture_engine:
        errors.append("CaptureEngine must save completed recording URLs as absoluteString")
    if "print(videoEntry)" in capture_engine:
        errors.append("CaptureEngine must not print saved recording metadata or file URLs")
    if "bitdash-a.akamaihd.net" in player_viewer or "URL(string: \"http" in player_viewer:
        errors.append("PlayerViewer must not hardcode remote playback URLs")
    if "URL(string:" in player_viewer and "!" in player_viewer:
        errors.append("PlayerViewer must not force unwrap URL(string:) values")
    if "func load(url: URL)" not in player_viewer:
        errors.append("PlayerViewer must load caller-provided recording URLs")
    if 'NSPersistentContainer(name: "CaptureSample")' in persistence_controller:
        errors.append("PersistenceController must use the checked-in Video Core Data model")
    if "fatalError(" in persistence_controller:
        errors.append("PersistenceController must not crash on persistent store load failures")
    if 'NSPersistentContainer(name: "Video")' not in persistence_controller:
        errors.append("PersistenceController must initialize the Video Core Data model")
    if "import OSLog" not in persistence_controller or "private let logger = Logger()" not in persistence_controller:
        errors.append("PersistenceController must use structured logging for persistence failures")
    if 'logger.error("Core Data failed to load:' not in persistence_controller:
        errors.append("PersistenceController must log persistent store load failures")
    if "func refreshTimer(now: Date = Date())" not in screen_recorder:
        errors.append("ScreenRecorder must centralize recording timer refreshes")
    if "private func resetTimer()" not in screen_recorder:
        errors.append("ScreenRecorder must centralize recording timer reset behavior")
    if "timerString = now.passedTime(from: startTime)" not in screen_recorder:
        errors.append("ScreenRecorder timer refresh must derive elapsed time from startTime")
    if "resetTimer()\n        recordTimer = Timer.publish" not in screen_recorder:
        errors.append("ScreenRecorder.start must reset the visible timer before restarting the publisher")
    if 'logger.error("Cannot start capture without a selected source.")\n                stopAudioMetering()\n                resetTimer()\n                return' not in screen_recorder:
        errors.append("ScreenRecorder.start must stop audio metering and reset the timer when no capture source is selected")
    if 'logger.error("\\(error.localizedDescription)")\n            stopAudioMetering()\n            resetTimer()\n            // Unable to start the stream. Set the running state to false.' not in screen_recorder:
        errors.append("ScreenRecorder.start must stop audio metering and reset the timer when capture startup throws")
    if "isRunning = false\n        startTime = Date()\n        resetTimer()" not in screen_recorder:
        errors.append("ScreenRecorder.stop must reset the visible timer after recording completes")
    if '@AppStorage("timerString")' in capture_app:
        errors.append("CaptureSampleApp must not keep a separate menu bar timer string")
    if "Text(screenRecorder.timerString)" not in capture_app:
        errors.append("CaptureSampleApp menu bar must display ScreenRecorder.timerString")
    if "screenRecorder.refreshTimer()" not in capture_app:
        errors.append("CaptureSampleApp menu bar must refresh the centralized timer")
    if "@State private var timerString" in menu_view or "Text(self.timerString)" in menu_view:
        errors.append("MenuView must not keep a stale local timer string")
    if "@Binding var userStopped: Bool" not in menu_view:
        errors.append("MenuView must bind userStopped so menu actions update shared recording state")
    if "if (!userStopped)" in menu_view or "if (userStopped)" in menu_view:
        errors.append("MenuView recording toggle must use one stop/start branch")
    if "Text(screenRecorder.timerString)" not in menu_view:
        errors.append("MenuView must display ScreenRecorder.timerString")
    if "screenRecorder.refreshTimer()" not in menu_view:
        errors.append("MenuView must refresh the centralized timer")

    for swift_path in sorted((ROOT / "CaptureSample").rglob("*.swift")):
        for line_number, line in enumerate(swift_path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
                continue
            if "print(" in stripped:
                errors.append(f"{swift_path.relative_to(ROOT)}:{line_number} must not use print(...) for app logging")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("project", "behavior"), required=True)
    args = parser.parse_args()

    errors = project_checks() if args.mode == "project" else behavior_checks()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"{args.mode} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
