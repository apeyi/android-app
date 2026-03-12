import SwiftUI

@main
struct FBAudioApp: App {
    @StateObject private var player = AudioPlayer.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(player)
                .tint(.saffronOrange)
        }
    }
}
