//
//  PlayerViewer.swift
//  CaptureSample
//
//  Created by gpj on 11/25/22.
//  Copyright © 2022 Apple. All rights reserved.
//

import Foundation
import AVKit

class PlayerViewer: View {
  private let playerLayer = AVPlayerLayer()
  override init(frame: CGRect) {
    super.init(frame: frame)

    let url = URL(string: "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8")!
    let player = AVPlayer(url: url)
    player.play()

    playerLayer.player = player
    layer.addSublayer(playerLayer)
  }
  required init?(coder: NSCoder) {
   fatalError("init(coder:) has not been implemented")
  }
  override func layoutSubviews() {
    super.layoutSubviews()
    playerLayer.frame = bounds
  }
}
