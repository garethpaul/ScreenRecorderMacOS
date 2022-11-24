/*
See LICENSE folder for this sample’s licensing information.

Abstract:
The entry point into this app.
*/
import SwiftUI

@main
struct CaptureSampleApp: App {
    @State var currentNumber: String = "1"
    @StateObject var screenRecorder = ScreenRecorder()
    @State var userStopped: Bool = false

    var body: some Scene {
        WindowGroup {
            ContentView(screenRecorder: screenRecorder)
                .frame(minWidth: 960, minHeight: 724)
                .background(.black)
        }
        MenuBarExtra(currentNumber, systemImage: "record.circle"){
            Button {
                Task { await screenRecorder.start() }
                // Fades the paused screen out.
                withAnimation(Animation.easeOut(duration: 0.25)) {
                    userStopped = true
                }
            } label: {
                Text("\(screenRecorder.isRunning.description)")
            }
            //.disabled(!screenRecorder.isRunning)
            Button {
                Task { await screenRecorder.stop() }
                // Fades the paused screen in.
                withAnimation(Animation.easeOut(duration: 0.25)) {
                    userStopped = true
                }

            } label: {
                Text("Stop Capture")
            }
            //.disabled(screenRecorder.isRunning)

        }
    }
}
