#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-screen-recorder-macos-baseline.md"


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require_paths():
    missing = []
    for relative_path in (
        "ScreenRecorder.xcodeproj/project.pbxproj",
        "ScreenRecorder.xcodeproj/xcshareddata/xcschemes/CaptureSample.xcscheme",
        "CaptureSample/CaptureEngine.swift",
        "CaptureSample/ScreenRecorder.swift",
        "CaptureSample/ContentView.swift",
        "CaptureSample/Record.swift",
        "CaptureSample/CaptureSample.entitlements",
    ):
        if not (ROOT / relative_path).exists():
            missing.append(f"missing required project file: {relative_path}")
    return missing


def docs_plan_checks():
    errors = []
    if not CANONICAL_PLAN.exists():
        errors.append("docs/plans/2026-06-08-screen-recorder-macos-baseline.md is missing")

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
    content_view = read_text("CaptureSample/ContentView.swift")
    record = read_text("CaptureSample/Record.swift")

    if "import ScreenCaptureKit" not in capture_engine:
        errors.append("CaptureEngine.swift must import ScreenCaptureKit")
    if "func startCapture(" not in capture_engine or "func stopCapture()" not in capture_engine:
        errors.append("CaptureEngine must expose start and stop capture operations")
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
