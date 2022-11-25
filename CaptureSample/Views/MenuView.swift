//
//  MenuView.swift
//  CaptureSample
//
//  Created by gpj on 11/24/22.
//  Copyright © 2022 Apple. All rights reserved.
//

import Foundation
import SwiftUI

struct MenuView: View {
    @ObservedObject var screenRecorder: ScreenRecorder
    @State var currentFocus: String
    @State var userStopped: Bool
    @State private var timerString = "00:00"

    var body: some View {
        ScrollView{
            VStack(alignment: .leading) {
                Text("What are you focused on right now?")
                TextField("", text: $currentFocus)
                    .textFieldStyle(.squareBorder)
                HStack{
                    Spacer()
                    Button{
                        if (!userStopped) {
                            print("stopped")
                            Task {
                                await screenRecorder.stop()
                            }
                            self.userStopped = true
                        }
                        if (userStopped) {
                            print("start")
                            Task {
                                await screenRecorder.start()
                            }
                            self.userStopped = false
                        }
                    } label: {
                        VStack(alignment: .center){
                            Image(systemName: screenRecorder.isRunning == true ? "pause.fill" : "record.circle.fill")
                                      .resizable()
                                      .frame(width: 10, height: 10)
                                      .foregroundColor(.white)
                                      .padding(20)
                                      .background(screenRecorder.isRunning == true ? Color.gray : Color.red)
                                      .clipShape(Circle())
                            Text(screenRecorder.isRunning == true ? "Stop": "Record")
                            Text(self.timerString)
                                        .onReceive(screenRecorder.recordTimer) { _ in
                                            if screenRecorder.isRunning {
                                                timerString = Date().passedTime(from: screenRecorder.startTime)
                                            }
                                        }
                        }.padding()

                    }.buttonStyle(PlainButtonStyle())

                    Spacer()
                }

            }.onChange(of: screenRecorder.isRunning, perform: { newValue in
                print("changed")

            }).padding()
        }
    }
}
