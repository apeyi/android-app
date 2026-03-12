import SwiftUI

struct ContentView: View {
    @EnvironmentObject var player: AudioPlayer
    @State private var selectedTab = 0
    @State private var showPlayer = false
    @State private var navigationPath = NavigationPath()

    var body: some View {
        ZStack(alignment: .bottom) {
            TabView(selection: $selectedTab) {
                NavigationStack(path: $navigationPath) {
                    HomeScreen(
                        onTalkClick: { navigateToDetail($0) },
                        onSangharakshitaByYearClick: { navigateToBrowse(.sangharakshitaByYear) },
                        onSangharakshitaSeriesClick: { navigateToBrowse(.sangharakshitaSeries) },
                        onMitraStudyClick: { navigateToBrowse(.mitraStudy) },
                        onDonateClick: { openDonateUrl() }
                    )
                    .navigationTitle("Free Buddhist Audio")
                    .navigationDestination(for: Route.self) { route in
                        routeView(route)
                    }
                }
                .tabItem {
                    Label("Home", systemImage: "house")
                }
                .tag(0)

                NavigationStack {
                    SearchScreen(onTalkClick: { navigateToDetail($0) })
                }
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
                .tag(1)

                NavigationStack {
                    DownloadsScreen(onTalkClick: { navigateToDetail($0) })
                }
                .tabItem {
                    Label("Downloads", systemImage: "arrow.down.circle")
                }
                .tag(2)
            }

            // Mini player
            if !showPlayer {
                MiniPlayer(player: player, onExpand: { showPlayer = true })
                    .padding(.bottom, 49) // TabView height
            }
        }
        .fullScreenCover(isPresented: $showPlayer) {
            PlayerScreen(
                player: player,
                onNavigateToDetail: { catNum in
                    showPlayer = false
                    navigateToDetail(catNum)
                },
                onSpeakerClick: { speaker in
                    showPlayer = false
                    navigateToBrowse(.speaker(speaker))
                }
            )
        }
    }

    // MARK: - Navigation

    enum Route: Hashable {
        case detail(String)
        case browse(BrowseModeRoute)
        case transcript(String, String)
    }

    enum BrowseModeRoute: Hashable {
        case sangharakshitaByYear
        case sangharakshitaSeries
        case mitraStudy
        case speaker(String)
        case series(String)

        var toBrowseMode: BrowseScreen.BrowseMode {
            switch self {
            case .sangharakshitaByYear: return .sangharakshitaByYear
            case .sangharakshitaSeries: return .sangharakshitaSeries
            case .mitraStudy: return .mitraStudy
            case .speaker(let name): return .speaker(name)
            case .series(let url): return .series(url)
            }
        }
    }

    private func navigateToDetail(_ catNum: String) {
        navigationPath.append(Route.detail(catNum))
    }

    private func navigateToBrowse(_ mode: BrowseModeRoute) {
        navigationPath.append(Route.browse(mode))
    }

    @ViewBuilder
    private func routeView(_ route: Route) -> some View {
        switch route {
        case .detail(let catNum):
            DetailScreen(
                catNum: catNum,
                onPlay: { catNum in
                    Task {
                        if let talk = await TalkRepository.shared.getTalkDetail(catNum) {
                            player.playTalk(talk)
                        }
                    }
                },
                onSpeakerClick: { navigateToBrowse(.speaker($0)) },
                onSeriesClick: { navigateToBrowse(.series($0)) },
                onTranscriptClick: { url, catNum in
                    navigationPath.append(Route.transcript(url, catNum))
                }
            )
        case .browse(let mode):
            BrowseScreen(
                initialMode: mode.toBrowseMode,
                onTalkClick: { navigateToDetail($0) }
            )
        case .transcript(let url, let catNum):
            TranscriptScreen(transcriptUrl: url, catNum: catNum)
        }
    }

    private func openDonateUrl() {
        if let url = URL(string: "https://www.freebuddhistaudio.com/donate/") {
            UIApplication.shared.open(url)
        }
    }
}
