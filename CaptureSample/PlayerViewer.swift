//
//  PlayerViewer.swift
//  CaptureSample
//
//  Created by gpj on 11/25/22.
//  Copyright © 2022 Apple. All rights reserved.
//

import Foundation
import AppKit
import AVKit

class PlayerViewer: NSView {
    private let playerLayer = AVPlayerLayer()
    private var player: AVPlayer?

    override init(frame: CGRect) {
        super.init(frame: frame)
        configureLayer()
    }

    convenience init(frame: CGRect, url: URL) {
        self.init(frame: frame)
        load(url: url)
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        configureLayer()
    }

    func load(url: URL) {
        let player = AVPlayer(url: url)
        self.player = player
        playerLayer.player = player
    }

    func play() {
        player?.play()
    }

    func pause() {
        player?.pause()
    }

    override func layout() {
        super.layout()
        playerLayer.frame = bounds
    }

    private func configureLayer() {
        wantsLayer = true
        layer = playerLayer
    }
}
