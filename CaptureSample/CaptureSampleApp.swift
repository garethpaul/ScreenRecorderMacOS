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
    @AppStorage("userStopped") var userStopped: Bool = false
    @AppStorage("currentFocus") var currentFocus: String = ""
    @State var switcher: Bool = false

    var body: some Scene {
        WindowGroup {
            ContentView(userStopped: userStopped, screenRecorder: screenRecorder)
                .frame(minWidth: 960, minHeight: 724)
                .background(.black)
                .environment(\.managedObjectContext, DataController.shared.moc)
        }.windowStyle(HiddenTitleBarWindowStyle())

        MenuBarExtra{
            MenuView(screenRecorder: screenRecorder, currentFocus: currentFocus, userStopped: $userStopped)
        }label: {
            Text(screenRecorder.timerString)
                        .font(Font.system(.largeTitle, design: .monospaced))
                        .onReceive(screenRecorder.recordTimer) { _ in
                            screenRecorder.refreshTimer()
                        }
        }
        .menuBarExtraStyle(.window)
    }
}
