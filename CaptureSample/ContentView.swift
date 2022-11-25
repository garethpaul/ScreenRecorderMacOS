/*
See LICENSE folder for this sample’s licensing information.

Abstract:
The app's main view.
*/

import SwiftUI
import ScreenCaptureKit
import OSLog
import Combine

struct ContentView: View {

    @AppStorage("userStopped") var userStopped: Bool = false
    @State var disableInput = false
    @State var isUnauthorized = false
    @ObservedObject var screenRecorder: ScreenRecorder

    var body: some View {
         TabView {
            ConfigurationView(screenRecorder: screenRecorder, userStopped: $userStopped)
                .frame(minWidth: 280, maxWidth: 280)
                .disabled(disableInput)
                .tabItem {
                            Label("Configuration", systemImage: "tray.and.arrow.down")
                        }

            screenRecorder.capturePreview
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .aspectRatio(screenRecorder.contentSize, contentMode: .fit)
                .padding(8)
                .overlay {
                    if userStopped {
                        Image(systemName: "nosign")
                            .font(.system(size: 250, weight: .bold))
                            .foregroundColor(Color(white: 0.3, opacity: 1.0))
                            .frame(maxWidth: .infinity, maxHeight: .infinity)
                            .background(Color(white: 0.0, opacity: 0.5))
                    }
                }
                .tabItem {
                            Label("Preview", systemImage: "tray.and.arrow.down")
                        }
        }
        .overlay {
            if isUnauthorized {
                VStack() {
                    Spacer()
                    VStack {
                        Text("No screen recording permission.")
                            .font(.largeTitle)
                            .padding(.top)
                        Text("Open System Settings and go to Privacy & Security > Screen Recording to grant permission.")
                            .font(.title2)
                            .padding(.bottom)
                    }
                    .frame(maxWidth: .infinity)
                    .background(.red)
                    
                }
            }
        }
        .navigationTitle("Screen Recorder")
        .onAppear {
            Task {
                if await screenRecorder.canRecord {
                    await screenRecorder.start()
                } else {
                    isUnauthorized = true
                    disableInput = true
                }
            }
        }
    }
}
