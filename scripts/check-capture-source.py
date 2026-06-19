#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

from menu_recorder_state_contract import validation_errors as menu_state_errors
from movie_recorder_video_start_contract import validation_errors as video_start_errors
from screen_recorder_start_stop_contract import validation_errors as start_stop_errors
from stream_delegate_failure_contract import validation_errors as stream_delegate_errors
from user_stopped_autostart_contract import validation_errors as autostart_errors


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-screen-recorder-macos-baseline.md"
TIMER_RESET_PLAN = DOCS_PLANS / "2026-06-09-recording-timer-reset.md"
CI_PLAN = DOCS_PLANS / "2026-06-10-ci-baseline.md"
HOSTED_BUILD_PLAN = DOCS_PLANS / "2026-06-10-hosted-macos-build.md"
RECORDER_HANDOFF_PLAN = DOCS_PLANS / "2026-06-12-recorder-handoff-identity.md"
RECORDING_FINALIZATION_PLAN = DOCS_PLANS / "2026-06-12-recording-finalization-integrity.md"
AWAITED_FINALIZATION_PLAN = DOCS_PLANS / "2026-06-13-awaited-recording-finalization.md"
AUDIO_FORWARDING_PLAN = DOCS_PLANS / "2026-06-13-audio-sample-forwarding.md"
MAKE_ROOT_PLAN = DOCS_PLANS / "2026-06-14-make-root-override-protection.md"
WRITER_START_FAILURE_PLAN = DOCS_PLANS / "2026-06-14-writer-start-failure-propagation.md"
RUNTIME_WRITER_START_FAILURE_PLAN = DOCS_PLANS / "2026-06-14-runtime-writer-start-failure.md"
VIDEO_APPEND_FAILURE_PLAN = DOCS_PLANS / "2026-06-15-video-append-failure-propagation.md"
AUDIO_APPEND_FAILURE_PLAN = DOCS_PLANS / "2026-06-15-audio-append-failure-propagation.md"
RECORDER_SETTINGS_PLAN = DOCS_PLANS / "2026-06-16-recorder-settings-contract.md"
USER_STOPPED_AUTOSTART_PLAN = DOCS_PLANS / "2026-06-16-user-stopped-autostart-guard.md"
MENU_RECORDER_STATE_PLAN = DOCS_PLANS / "2026-06-16-menu-recorder-state-toggle.md"
STREAM_DELEGATE_FAILURE_PLAN = DOCS_PLANS / "2026-06-17-stream-delegate-failure-cleanup.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "check.yml"
MAKEFILE = ROOT / "Makefile"
CHECKOUT_ACTION = "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10"
SETUP_PYTHON_ACTION = "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405"
ALLOWED_ACTIONS = {"actions/checkout", "actions/setup-python"}


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
        str(WRITER_START_FAILURE_PLAN.relative_to(ROOT)),
        str(RUNTIME_WRITER_START_FAILURE_PLAN.relative_to(ROOT)),
        str(VIDEO_APPEND_FAILURE_PLAN.relative_to(ROOT)),
        str(AUDIO_APPEND_FAILURE_PLAN.relative_to(ROOT)),
        str(RECORDER_SETTINGS_PLAN.relative_to(ROOT)),
        str(USER_STOPPED_AUTOSTART_PLAN.relative_to(ROOT)),
        str(MENU_RECORDER_STATE_PLAN.relative_to(ROOT)),
        str(STREAM_DELEGATE_FAILURE_PLAN.relative_to(ROOT)),
        "scripts/test_movie_recorder_video_start_contract.py",
        "scripts/test_screen_recorder_start_stop_contract.py",
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
    if not CI_PLAN.exists():
        errors.append("docs/plans/2026-06-10-ci-baseline.md is missing")
    if not HOSTED_BUILD_PLAN.exists():
        errors.append("docs/plans/2026-06-10-hosted-macos-build.md is missing")
    if not RECORDER_HANDOFF_PLAN.exists():
        errors.append("docs/plans/2026-06-12-recorder-handoff-identity.md is missing")
    if not RECORDING_FINALIZATION_PLAN.exists():
        errors.append("docs/plans/2026-06-12-recording-finalization-integrity.md is missing")
    if not AWAITED_FINALIZATION_PLAN.exists():
        errors.append("docs/plans/2026-06-13-awaited-recording-finalization.md is missing")
    if not AUDIO_FORWARDING_PLAN.exists():
        errors.append("docs/plans/2026-06-13-audio-sample-forwarding.md is missing")
    if not MAKE_ROOT_PLAN.exists():
        errors.append("docs/plans/2026-06-14-make-root-override-protection.md is missing")

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

    if not CI_WORKFLOW.exists():
        errors.append(".github/workflows/check.yml is missing")
    else:
        workflow = CI_WORKFLOW.read_text(encoding="utf-8")
        if (
            workflow.count(f"uses: {CHECKOUT_ACTION}") != 2
            or workflow.count(f"uses: {SETUP_PYTHON_ACTION}") != 1
            or 'python-version: "3.12"' not in workflow
            or "runs-on: ubuntu-24.04" not in workflow
            or "runs-on: macos-15" not in workflow
            or "concurrency:" not in workflow
            or "cancel-in-progress: true" not in workflow
            or "permissions:\n  contents: read" not in workflow
            or workflow.count("persist-credentials: false") != 2
            or "timeout-minutes: 5" not in workflow
            or "timeout-minutes: 15" not in workflow
            or "  push:\n" not in workflow
            or "  pull_request:\n" not in workflow
            or "workflow_dispatch:" not in workflow
            or "pull_request_target:" in workflow
            or "branches:" in workflow
            or "run: make check" not in workflow
            or "run: make build" not in workflow
        ):
            errors.append(".github/workflows/check.yml must keep the pinned structural and macOS build baselines")
        for action, revision in re.findall(
            r"^\s*(?:-\s*)?uses:\s*([^@\s]+)@([^\s#]+)",
            workflow,
            flags=re.MULTILINE,
        ):
            if action not in ALLOWED_ACTIONS:
                errors.append(f"GitHub Actions action {action} is not approved")
            if not re.fullmatch(r"[a-f0-9]{40}", revision):
                errors.append(f"GitHub Actions action {action} must be pinned to a full commit SHA")

    makefile = MAKEFILE.read_text(encoding="utf-8") if MAKEFILE.exists() else ""
    root_declaration = "override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))"
    root_assignments = [
        line
        for line in makefile.splitlines()
        if re.match(r"^(?:override\s+)?ROOT\s*[:?+]?=", line)
    ]
    if not makefile.startswith(f"{root_declaration}\n") or root_assignments != [
        root_declaration
    ]:
        errors.append(
            "Makefile must define exactly one protected repository-derived ROOT declaration first"
        )
    for fragment in (
        root_declaration,
        '$(PYTHON) "$(ROOT)/scripts/check-capture-source.py" --mode project',
        '$(PYTHON) "$(ROOT)/scripts/test_movie_recorder_video_start_contract.py"',
        '$(PYTHON) "$(ROOT)/scripts/test_screen_recorder_start_stop_contract.py"',
        '$(PYTHON) "$(ROOT)/scripts/test_stream_delegate_failure_contract.py"',
        'cd "$(ROOT)" && "$(XCODEBUILD)" -project ScreenRecorder.xcodeproj',
        "CODE_SIGNING_ALLOWED=NO build",
    ):
        if fragment not in makefile:
            errors.append(f"Makefile must keep contract: {fragment}")

    if MAKE_ROOT_PLAN.exists():
        root_plan = MAKE_ROOT_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "`make ROOT=/tmp check` passed",
            "all five public Make aliases passed",
            "Six hostile mutations were rejected",
            "Python 3.12",
        ):
            if evidence not in root_plan:
                errors.append(
                    f"{MAKE_ROOT_PLAN.relative_to(ROOT)} must record verification evidence {evidence!r}"
                )
        if str(MAKE_ROOT_PLAN.relative_to(ROOT)) not in read_text("README.md"):
            errors.append(f"README.md must reference {MAKE_ROOT_PLAN.relative_to(ROOT)}")

    for docs_file in ("README.md", "VISION.md", "SECURITY.md", "CHANGES.md"):
        document = read_text(docs_file)
        if "GitHub Actions" not in document:
            errors.append(f"{docs_file} must document the GitHub Actions baseline")
        if "recorder handoff" not in document:
            errors.append(f"{docs_file} must document the recorder handoff contract")
        if "awaited recording finalization" not in document.lower():
            errors.append(f"{docs_file} must document awaited recording finalization")
        if "audio sample forwarding" not in document.lower():
            errors.append(f"{docs_file} must document audio sample forwarding")
        if "writer startup failure" not in document.lower():
            errors.append(f"{docs_file} must document writer startup failure propagation")
        if "runtime writer start failure" not in document.lower():
            errors.append(f"{docs_file} must document runtime writer start failure containment")
        if "video sample append failure" not in document.lower():
            errors.append(f"{docs_file} must document video sample append failure propagation")
    for docs_file in ("AGENTS.md", "README.md", "VISION.md", "SECURITY.md", "CHANGES.md"):
        raw_document = read_text(docs_file)
        if "Video and audio sample append failures propagate through the shared recording cleanup path." not in raw_document:
            errors.append(f"{docs_file} must document shared video/audio append failure cleanup")
        document = " ".join(raw_document.split())
        if "Unexpected ScreenCaptureKit delegate stops propagate through the shared recording cleanup path" not in document:
            errors.append(f"{docs_file} must document stream delegate failure cleanup")
        if (
            "MovieRecorder" not in document
            or "video transform" not in document
            or "fixed audio and video output settings" not in document
            or "startRecording" not in document
        ):
            errors.append(f"{docs_file} must document the recorder settings contract")

    entitlements = read_text("CaptureSample/CaptureSample.entitlements")
    if "<plist version=\"1.0\">" not in entitlements:
        errors.append("entitlements file is not an XML plist")

    return errors


def behavior_checks():
    errors = require_paths()
    if errors:
        return errors

    capture_engine = read_text("CaptureSample/CaptureEngine.swift")
    errors.extend(stream_delegate_errors(capture_engine))
    screen_recorder = read_text("CaptureSample/ScreenRecorder.swift")
    errors.extend(start_stop_errors(screen_recorder))
    capture_app = read_text("CaptureSample/CaptureSampleApp.swift")
    content_view = read_text("CaptureSample/ContentView.swift")
    errors.extend(autostart_errors(content_view))
    record = read_text("CaptureSample/Record.swift")
    errors.extend(video_start_errors(record))
    player_viewer = read_text("CaptureSample/PlayerViewer.swift")
    persistence_controller = read_text("CaptureSample/PersistenceController.swift")
    menu_view = read_text("CaptureSample/Views/MenuView.swift")
    errors.extend(menu_state_errors(menu_view))
    swift_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "CaptureSample").rglob("*.swift"))
    )

    if "init(videoTransform: CGAffineTransform)" not in record:
        errors.append("MovieRecorder must expose only the video transform at initialization")
    if "private let videoTransform: CGAffineTransform" not in record:
        errors.append("MovieRecorder must keep its initializer-only video transform immutable")
    for ignored_fragment in (
        "init(audioSettings:",
        "private var audioSettings",
        "private var videoSettings",
        "MovieRecorder(audioSettings:",
        "MovieRecorder(videoSettings:",
    ):
        if ignored_fragment in swift_source:
            errors.append(f"MovieRecorder must not retain ignored settings fragment {ignored_fragment!r}")
    initializer_call = "MovieRecorder(videoTransform: .identity)"
    if swift_source.count(initializer_call) != 2:
        errors.append("both recorder call sites must use the truthful video-transform initializer")
    for fixed_setting in (
        "AVFormatIDKey: kAudioFormatLinearPCM",
        "AVSampleRateKey: 44100",
        "AVNumberOfChannelsKey: 2",
        "AVLinearPCMBitDepthKey: 16",
        "AVVideoCodecKey: AVVideoCodecType.h264",
        "AVVideoWidthKey: width",
        "AVVideoHeightKey: height",
    ):
        if fixed_setting not in record:
            errors.append(f"MovieRecorder must retain fixed writer setting {fixed_setting!r}")

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
    if 'attachments[.contentRect] as? [String: NSNumber]' not in capture_engine:
        errors.append("CaptureEngine must validate content rectangle metadata as numeric dictionary values")
    audio_case = re.search(
        r"case \.audio, \.microphone:(.*?)(?=\n\s*@unknown default:)",
        capture_engine,
        re.DOTALL,
    )
    if not audio_case:
        errors.append("CaptureEngine must handle ScreenCaptureKit audio and microphone samples")
    else:
        audio_body = audio_case.group(1)
        required_audio_flow = (
            "guard let samples = createPCMBuffer(for: sampleBuffer) else { return }",
            "pcmBufferHandler?(samples)",
            "try movie?.recordAudio(sampleBuffer: sampleBuffer)",
            "recordingErrorHandler?(error)",
        )
        positions = [audio_body.find(fragment) for fragment in required_audio_flow]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            errors.append("CaptureEngine audio output must convert, meter, and forward the accepted sample in order")
        if audio_body.count("try movie?.recordAudio(sampleBuffer: sampleBuffer)") != 1:
            errors.append("CaptureEngine audio output must forward each accepted sample exactly once")
        if "do {" not in audio_body or "} catch {" not in audio_body:
            errors.append("CaptureEngine audio output must route recorder failures through the shared handler")
    for key in ("X", "Y", "Width", "Height"):
        if f'contentRectValues["{key}"]' not in capture_engine:
            errors.append(f"CaptureEngine must validate the content rectangle {key} value")
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
    if "func cancelRecording()" not in record:
        errors.append("MovieRecorder must expose startup-failure cancellation")
    if "assetWriter.cancelWriting()" not in record or "FileManager.default.removeItem(at: assetWriter.outputURL)" not in record:
        errors.append("MovieRecorder cancellation must cancel the writer and remove its partial file")
    if "self.movie.cancelRecording()\n                continuation.finish(throwing: error)" not in capture_engine:
        errors.append("CaptureEngine start failures must cancel the partial movie before finishing")
    if "func stopRecording() async -> URL?" not in record:
        errors.append("MovieRecorder stop must expose an awaitable completed-or-failed output URL")
    if "let assetWriter = self.assetWriter\n        isRecording = false\n        self.assetWriter = nil\n        assetWriterAudioInput = nil\n        assetWriterVideoInput = nil\n\n        guard let assetWriter = assetWriter else" not in record:
        errors.append("MovieRecorder stop must clear all recorder state before handling an absent writer")
    if "guard let assetWriter = assetWriter else {\n            return nil\n        }" not in record:
        errors.append("MovieRecorder stop must complete with no URL when no writer is active")
    if "guard assetWriter.status == .completed else {" not in record:
        errors.append("MovieRecorder stop must require completed writer status before returning an output URL")
    if "return await withCheckedContinuation { continuation in" not in record:
        errors.append("MovieRecorder stop must await AVAssetWriter finalization")
    if "continuation.resume(returning: nil)" not in record or "continuation.resume(returning: assetWriter.outputURL)" not in record:
        errors.append("MovieRecorder stop must resume awaited finalization for failed and completed outputs")
    if "guard assetWriter.status == .completed else {\n                    try? FileManager.default.removeItem(at: assetWriter.outputURL)" not in record:
        errors.append("MovieRecorder stop must remove the partial output when finalization fails")
    if "guard let url = await self.movie.stopRecording() else {\n            return\n        }\n\n        // save to CoreData" not in capture_engine:
        errors.append("CaptureEngine must not persist metadata without a completed recording URL")
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
    if "streamOutput.movie!" in capture_engine:
        errors.append("CaptureEngine must not force unwrap the recorder during handoff")
    if "streamOutput.movie = movie" not in capture_engine or "self.movie = movie" not in capture_engine:
        errors.append("CaptureEngine and stream output must share the caller-provided recorder")
    if "enum MovieRecorderError: Error" not in record or "case documentDirectoryUnavailable" not in record:
        errors.append("MovieRecorder must define an explicit output-directory startup error")
    if "func startRecording(height: Int, width: Int) throws" not in record:
        errors.append("MovieRecorder.startRecording must propagate writer startup failures")
    if "throw MovieRecorderError.documentDirectoryUnavailable" not in record:
        errors.append("MovieRecorder must propagate missing output-directory failures")
    if "let assetWriter = try AVAssetWriter(url: outputFileURL, fileType: .mov)" not in record:
        errors.append("MovieRecorder must propagate AVAssetWriter creation failures")
    for fragment in (
        "case assetWriterStartFailed",
        "func recordVideo(sampleBuffer: CMSampleBuffer) throws",
        "guard assetWriter.startWriting() else {",
        "throw assetWriter.error ?? MovieRecorderError.assetWriterStartFailed",
    ):
        if fragment not in record:
            errors.append(f"MovieRecorder must propagate runtime writer start failures via {fragment!r}")
    for fragment in (
        "case assetWriterAppendFailed",
        "guard input.append(sampleBuffer) else {",
        "throw assetWriter.error ?? MovieRecorderError.assetWriterAppendFailed",
    ):
        if fragment not in record:
            errors.append(f"MovieRecorder must propagate video sample append failures via {fragment!r}")
    audio_record = re.search(
        r"func recordAudio\(sampleBuffer: CMSampleBuffer\) throws \{(.*?)\n    \}",
        record,
        re.DOTALL,
    )
    if not audio_record:
        errors.append("MovieRecorder.recordAudio must remain a throwing method")
    else:
        audio_record_body = audio_record.group(1)
        for fragment in (
            "guard input.append(sampleBuffer) else {",
            "throw assetWriter.error ?? MovieRecorderError.assetWriterAppendFailed",
        ):
            if fragment not in audio_record_body:
                errors.append(f"MovieRecorder.recordAudio must propagate append failure via {fragment!r}")
    for fragment in (
        "streamOutput.recordingErrorHandler = { [weak self] error in",
        "self?.failCapture(error)",
        "private func failCapture(_ error: Error)",
        "movie.cancelRecording()\n        continuation?.finish(throwing: error)",
        "let stream = self.stream\n        self.stream = nil",
        "try? await stream?.stopCapture()",
        "var recordingErrorHandler: ((Error) -> Void)?",
        "try movie?.recordVideo(sampleBuffer: sampleBuffer)",
        "recordingErrorHandler?(error)",
    ):
        if fragment not in capture_engine:
            errors.append(f"CaptureEngine must contain runtime writer failure via {fragment!r}")
    writer_start = capture_engine.find("try self.movie.startRecording(")
    stream_start = capture_engine.find("stream = SCStream(")
    failure_cleanup = capture_engine.find("self.movie.cancelRecording()")
    if min(writer_start, stream_start, failure_cleanup) < 0 or not writer_start < stream_start < failure_cleanup:
        errors.append("CaptureEngine must start the writer before SCStream and retain failure cleanup")
    if WRITER_START_FAILURE_PLAN.exists():
        writer_plan = WRITER_START_FAILURE_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "repository and external-directory `make check` passed",
            "hostile writer startup mutations were rejected",
            "generated-artifact, recording-file, and credential-pattern audits passed",
        ):
            if evidence not in writer_plan:
                errors.append(
                    f"{WRITER_START_FAILURE_PLAN.relative_to(ROOT)} must record verification evidence {evidence!r}"
                )
    if RUNTIME_WRITER_START_FAILURE_PLAN.exists():
        runtime_writer_plan = RUNTIME_WRITER_START_FAILURE_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "repository and external-directory `make check` passed",
            "hostile runtime writer mutations were rejected",
            "generated-artifact, recording-file, and credential-pattern audits passed",
        ):
            if evidence not in runtime_writer_plan:
                errors.append(
                    f"{RUNTIME_WRITER_START_FAILURE_PLAN.relative_to(ROOT)} must record verification evidence {evidence!r}"
                )
    if VIDEO_APPEND_FAILURE_PLAN.exists():
        append_failure_plan = VIDEO_APPEND_FAILURE_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "repository and external-directory `make check` passed",
            "hostile video append mutations were rejected",
            "generated-artifact, recording-file, and credential-pattern audits passed",
        ):
            if evidence not in append_failure_plan:
                errors.append(
                    f"{VIDEO_APPEND_FAILURE_PLAN.relative_to(ROOT)} must record verification evidence {evidence!r}"
                )
    if AUDIO_APPEND_FAILURE_PLAN.exists():
        audio_append_plan = AUDIO_APPEND_FAILURE_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "repository and external-directory `make check` passed",
            "hostile audio append mutations were rejected",
            "generated-artifact, recording-file, and credential-pattern audits passed",
        ):
            if evidence not in audio_append_plan:
                errors.append(
                    f"{AUDIO_APPEND_FAILURE_PLAN.relative_to(ROOT)} must record verification evidence {evidence!r}"
                )
    if RECORDER_SETTINGS_PLAN.exists():
        settings_plan = RECORDER_SETTINGS_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "repository and external-directory `make check` passed",
            "hostile recorder settings mutations were rejected",
            "generated-artifact, recording-file, and credential-pattern audits passed",
        ):
            if evidence not in settings_plan:
                errors.append(
                    f"{RECORDER_SETTINGS_PLAN.relative_to(ROOT)} must record verification evidence {evidence!r}"
                )
    if USER_STOPPED_AUTOSTART_PLAN.exists():
        autostart_plan = USER_STOPPED_AUTOSTART_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "repository and external-directory `make check` passed",
            "four persisted-stop mutations were rejected",
            "generated-artifact, recording-file, and credential-pattern audits passed",
        ):
            if evidence not in autostart_plan:
                errors.append(
                    f"{USER_STOPPED_AUTOSTART_PLAN.relative_to(ROOT)} must record verification evidence {evidence!r}"
                )
    if MENU_RECORDER_STATE_PLAN.exists():
        menu_state_plan = MENU_RECORDER_STATE_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "repository and external-directory `make check` passed",
            "six recorder-state mutations were rejected",
            "generated-artifact, recording-file, and credential-pattern audits passed",
        ):
            if evidence not in menu_state_plan:
                errors.append(
                    f"{MENU_RECORDER_STATE_PLAN.relative_to(ROOT)} must record verification evidence {evidence!r}"
                )
    if STREAM_DELEGATE_FAILURE_PLAN.exists():
        stream_delegate_plan = STREAM_DELEGATE_FAILURE_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "repository and external-directory `make check` passed",
            "six stream-delegate mutations were rejected",
            "generated-artifact, recording-file, and credential-pattern audits passed",
        ):
            if evidence not in stream_delegate_plan:
                errors.append(
                    f"{STREAM_DELEGATE_FAILURE_PLAN.relative_to(ROOT)} must record verification evidence {evidence!r}"
                )
        if str(STREAM_DELEGATE_FAILURE_PLAN.relative_to(ROOT)) not in read_text("README.md"):
            errors.append(
                f"README.md must reference {STREAM_DELEGATE_FAILURE_PLAN.relative_to(ROOT)}"
            )
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
