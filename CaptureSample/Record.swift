import SwiftUI

import Foundation
import AVFoundation

class AudioRecorder {
    
    private var assetWriter: AVAssetWriter?
    
    private var assetWriterAudioInput: AVAssetWriterInput?
    
    private var audioSettings: [String: Any]
    
    // can be read from anywhere (getter) but only modified in this class (setter)
    private(set) var isRecording = false
    
    init(audioSettings: [String:Any]) {
        self.audioSettings = audioSettings
    }
    
    private func documentDirectory() -> String {
        let documentDirectory = NSSearchPathForDirectoriesInDomains(.documentDirectory,
                                                                    .userDomainMask,
                                                                    true)
        return documentDirectory[0]
    }
    
    private func append(toPath path: String,
                        withPathComponent pathComponent: String) -> String? {
        if var pathURL = URL(string: path) {
            pathURL.appendPathComponent(pathComponent)

            return pathURL.absoluteString
        }

        return nil
    }
    
    func startRecording() {
        let outputFileName = NSUUID().uuidString
        let filePath = self.append(toPath: self.documentDirectory(),
                                             withPathComponent: outputFileName)
        let outputFileURL = URL(fileURLWithPath: filePath!).appendingPathExtension("WAV")
        guard let assetWriter = try? AVAssetWriter(url: outputFileURL, fileType: .wav) else {
            return
        }

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

        self.assetWriter = assetWriter
        self.assetWriterAudioInput = assetWriterAudioInput

        isRecording = true
    }

    func stopRecording(completion: @escaping (URL) -> Void) {
        guard let assetWriter = assetWriter else {
            return
        }

        self.isRecording = false
        self.assetWriter = nil

        assetWriter.finishWriting {
            completion(assetWriter.outputURL)
        }
    }
    
    func recordAudio(sampleBuffer: CMSampleBuffer) {
        guard isRecording,
            let assetWriter = assetWriter else {
                return
        }

        if assetWriter.status == .unknown {
            assetWriter.startWriting()
            assetWriter.startSession(atSourceTime: CMSampleBufferGetPresentationTimeStamp(sampleBuffer))
        } else if assetWriter.status == .writing {
            if let input = assetWriterAudioInput,
                input.isReadyForMoreMediaData {
                input.append(sampleBuffer)
            }
        }
    }
    
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

    private func documentDirectory() -> String {
        let documentDirectory = NSSearchPathForDirectoriesInDomains(.documentDirectory,
                                                                    .userDomainMask,
                                                                    true)
        return documentDirectory[0]
    }

    private func append(toPath path: String,
                        withPathComponent pathComponent: String) -> String? {
        if var pathURL = URL(string: path) {
            pathURL.appendPathComponent(pathComponent)

            return pathURL.absoluteString
        }

        return nil
    }

    func startRecording(height: Int, width: Int) {
        // Create an asset writer that records to a temporary file
        let outputFileName = NSUUID().uuidString
        let filePath = self.append(toPath: self.documentDirectory(),
                                             withPathComponent: outputFileName)
        let outputFileURL = URL(fileURLWithPath: filePath!).appendingPathExtension("MOV")
        guard let assetWriter = try? AVAssetWriter(url: outputFileURL, fileType: .mov) else {
            return
        }

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

    func stopRecording(completion: @escaping (URL) -> Void) {
        guard let assetWriter = assetWriter else {
            return
        }

        self.isRecording = false
        self.assetWriter = nil

        assetWriter.finishWriting {
            completion(assetWriter.outputURL)
        }
    }

    func recordVideo(sampleBuffer: CMSampleBuffer) {
        guard isRecording,
            let assetWriter = assetWriter else {
                return
        }

        if assetWriter.status == .unknown {
            assetWriter.startWriting()
            assetWriter.startSession(atSourceTime: CMSampleBufferGetPresentationTimeStamp(sampleBuffer))
        } else if assetWriter.status == .writing {
            if let input = assetWriterVideoInput,
                input.isReadyForMoreMediaData {
                input.append(sampleBuffer)
            }
        }
    }

    func recordAudio(sampleBuffer: CMSampleBuffer) {
        guard isRecording,
            let assetWriter = assetWriter,
            assetWriter.status == .writing,
            let input = assetWriterAudioInput,
            input.isReadyForMoreMediaData else {
                return
        }

        input.append(sampleBuffer)
    }
}
