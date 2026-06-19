#!/usr/bin/env python3


def _record_video_body(source):
    marker = "func recordVideo(sampleBuffer: CMSampleBuffer) throws {"
    start = source.find(marker)
    if start < 0:
        return None
    end = source.find("\n    func recordAudio", start)
    if end < 0:
        return None
    return source[start:end]


def validation_errors(source):
    body = _record_video_body(source)
    if body is None:
        return ["MovieRecorder.recordVideo must remain a throwing method"]

    required_order = (
        "if assetWriter.status == .unknown {",
        "guard assetWriter.startWriting() else {",
        "assetWriter.startSession(atSourceTime: CMSampleBufferGetPresentationTimeStamp(sampleBuffer))",
        "guard assetWriter.status == .writing,",
        "let input = assetWriterVideoInput,",
        "input.isReadyForMoreMediaData else {",
        "guard input.append(sampleBuffer) else {",
        "throw assetWriter.error ?? MovieRecorderError.assetWriterAppendFailed",
    )
    positions = [body.find(fragment) for fragment in required_order]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        return [
            "MovieRecorder.recordVideo must start the writer, open the session, "
            "and append the same first video sample through the normal append guard"
        ]

    if body.count("input.append(sampleBuffer)") != 1:
        return ["MovieRecorder.recordVideo must append each accepted video sample exactly once"]

    if "} else if assetWriter.status == .writing {" in body:
        return [
            "MovieRecorder.recordVideo must not skip first-sample append behind an else-if branch"
        ]

    return []
