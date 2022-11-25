/*
See LICENSE folder for this sample’s licensing information.

Abstract:
The entry point into this app.
*/
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
            }.onChange(of: screenRecorder.isRunning, perform: { newValue in
                print("changed")

            }).padding()
        }
    }
}

@main
struct CaptureSampleApp: App {
    @State var currentNumber: String = "1"
    @StateObject var screenRecorder = ScreenRecorder()
    @AppStorage("userStopped") var userStopped: Bool = false
    @AppStorage("currentFocus") var currentFocus: String = ""
    @State var switcher: Bool = false

    @AppStorage("timerString") var timerString = "00:00"


    var body: some Scene {
        WindowGroup {
            ContentView(userStopped: userStopped, screenRecorder: screenRecorder)
                .frame(minWidth: 960, minHeight: 724)
                .background(.black)
        }.windowStyle(HiddenTitleBarWindowStyle())
        MenuBarExtra{
            MenuView(screenRecorder: screenRecorder, currentFocus: currentFocus, userStopped: userStopped)
        }label: {
            Text(self.timerString)
                        .font(Font.system(.largeTitle, design: .monospaced))
                        .onReceive(screenRecorder.recordTimer) { _ in
                            if screenRecorder.isRunning {
                                timerString = Date().passedTime(from: screenRecorder.startTime)
                            }
                        }
        }
        .menuBarExtraStyle(.window)

        
    }
}
