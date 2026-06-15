import SwiftUI

import Foundation
import AVFoundation

enum MovieRecorderError: Error {
    case documentDirectoryUnavailable
    case assetWriterStartFailed
    case assetWriterAppendFailed
}

class MovieRecorder {

    private var assetWriter: AVAssetWriter?

    private var assetWriterVideoInput: AVAssetWriterInput?

    private var assetWriterAudioInput: AVAssetWriterInput?

    private var videoTransform: CGAffineTransform

    private var videoSettings: [String: Any]

    private var audioSettings: [String: Any]

    private(set) var isRecording = false

    init(audioSettings: [String: Any], videoSettings: [String: Any], videoTransform: CGAffineTransform) {
        self.audioSettings = audioSettings
        self.videoSettings = videoSettings
        self.videoTransform = videoTransform
    }

    private func documentDirectory() -> URL? {
        FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first
    }

    func startRecording(height: Int, width: Int) throws {
        // Create an asset writer that records to a temporary file
        let outputFileName = NSUUID().uuidString
        guard let outputFileURL = documentDirectory()?
            .appendingPathComponent(outputFileName)
            .appendingPathExtension("MOV") else {
            throw MovieRecorderError.documentDirectoryUnavailable
        }
        let assetWriter = try AVAssetWriter(url: outputFileURL, fileType: .mov)

        // Add an audio input
        // Add an audio input
        let audioSettings = [
                    AVFormatIDKey: kAudioFormatLinearPCM,
                    AVSampleRateKey: 44100,
                    AVNumberOfChannelsKey: 2,
                    AVLinearPCMBitDepthKey: 16,
                    AVLinearPCMIsNonInterleaved: false,
                    AVLinearPCMIsFloatKey: false,
                    AVLinearPCMIsBigEndianKey: false
                ] as [String : Any]

        let assetWriterAudioInput = AVAssetWriterInput(mediaType: .audio, outputSettings: audioSettings)
        assetWriterAudioInput.expectsMediaDataInRealTime = true
        assetWriter.add(assetWriterAudioInput)

        let videoSettings = [
            AVVideoCodecKey: AVVideoCodecType.h264,
                    AVVideoWidthKey: width,
                    AVVideoHeightKey: height
                ] as [String : Any]

        // Add a video input
        let assetWriterVideoInput = AVAssetWriterInput(mediaType: .video, outputSettings: videoSettings)
        assetWriterVideoInput.expectsMediaDataInRealTime = true
        assetWriterVideoInput.transform = videoTransform
        assetWriter.add(assetWriterVideoInput)

        self.assetWriter = assetWriter
        self.assetWriterAudioInput = assetWriterAudioInput
        self.assetWriterVideoInput = assetWriterVideoInput

        isRecording = true
    }

    func stopRecording() async -> URL? {
        let assetWriter = self.assetWriter
        isRecording = false
        self.assetWriter = nil
        assetWriterAudioInput = nil
        assetWriterVideoInput = nil

        guard let assetWriter = assetWriter else {
            return nil
        }

        return await withCheckedContinuation { continuation in
            assetWriter.finishWriting {
                guard assetWriter.status == .completed else {
                    try? FileManager.default.removeItem(at: assetWriter.outputURL)
                    continuation.resume(returning: nil)
                    return
                }
                continuation.resume(returning: assetWriter.outputURL)
            }
        }
    }

    func cancelRecording() {
        guard let assetWriter = assetWriter else {
            isRecording = false
            return
        }

        isRecording = false
        self.assetWriter = nil
        assetWriterAudioInput = nil
        assetWriterVideoInput = nil
        assetWriter.cancelWriting()
        try? FileManager.default.removeItem(at: assetWriter.outputURL)
    }

    func recordVideo(sampleBuffer: CMSampleBuffer) throws {
        guard isRecording,
            let assetWriter = assetWriter else {
                return
        }

        if assetWriter.status == .unknown {
            guard assetWriter.startWriting() else {
                throw assetWriter.error ?? MovieRecorderError.assetWriterStartFailed
            }
            assetWriter.startSession(atSourceTime: CMSampleBufferGetPresentationTimeStamp(sampleBuffer))
        } else if assetWriter.status == .writing {
            if let input = assetWriterVideoInput,
                input.isReadyForMoreMediaData {
                guard input.append(sampleBuffer) else {
                    throw assetWriter.error ?? MovieRecorderError.assetWriterAppendFailed
                }
            }
        }
    }

    func recordAudio(sampleBuffer: CMSampleBuffer) throws {
        guard isRecording,
            let assetWriter = assetWriter,
            assetWriter.status == .writing,
            let input = assetWriterAudioInput,
            input.isReadyForMoreMediaData else {
                return
        }

        guard input.append(sampleBuffer) else {
            throw assetWriter.error ?? MovieRecorderError.assetWriterAppendFailed
        }
    }
}
