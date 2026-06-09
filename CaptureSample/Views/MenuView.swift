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
    @Binding var userStopped: Bool

    var body: some View {
        ScrollView{
            VStack(alignment: .leading) {
                Text("What are you focused on right now?")
                TextField("", text: $currentFocus)
                    .textFieldStyle(.squareBorder)
                HStack{
                    Spacer()
                    Button{
                        if userStopped {
                            Task {
                                await screenRecorder.start()
                            }
                            self.userStopped = false
                        } else {
                            Task {
                                await screenRecorder.stop()
                            }
                            self.userStopped = true
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
                            Text(screenRecorder.timerString)
                                        .onReceive(screenRecorder.recordTimer) { _ in
                                            screenRecorder.refreshTimer()
                                        }
                        }.padding()

                    }.buttonStyle(PlainButtonStyle())

                    Spacer()
                }

            }.padding()
        }
    }
}
