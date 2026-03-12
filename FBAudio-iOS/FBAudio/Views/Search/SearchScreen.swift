import SwiftUI

struct SearchScreen: View {
    @State private var query = ""
    @State private var results: [SearchResult] = []
    @State private var isLoading = false
    @State private var error: String?
    @State private var hasSearched = false

    let onTalkClick: (String) -> Void

    var body: some View {
        List {
            Section {
                TextField("Search or paste URL", text: $query)
                    .textFieldStyle(.roundedBorder)
                    .onSubmit { search() }
                    .autocorrectionDisabled()
            }

            if isLoading {
                ProgressView().frame(maxWidth: .infinity)
            } else if let error {
                VStack(spacing: 8) {
                    Text(error).foregroundStyle(.secondary)
                    Button("Retry") { search() }
                }
            } else if hasSearched && results.isEmpty {
                Text("No results found for \"\(query)\"")
                    .foregroundStyle(.secondary)
            } else {
                ForEach(results) { result in
                    TalkCard(
                        title: result.title,
                        speaker: result.speaker,
                        imageUrl: result.imageUrl,
                        subtitle: result.year > 0 ? "\(result.year)" : nil,
                        onClick: { onTalkClick(result.catNum) }
                    )
                    .listRowInsets(EdgeInsets(top: 4, leading: 16, bottom: 4, trailing: 16))
                    .listRowSeparator(.hidden)
                }
            }
        }
        .listStyle(.plain)
        .navigationTitle("Search")
    }

    private func search() {
        guard !query.trimmingCharacters(in: .whitespaces).isEmpty else { return }
        isLoading = true
        error = nil
        Task {
            do {
                results = try await TalkRepository.shared.searchAudio(query)
                hasSearched = true
            } catch {
                self.error = friendlyError(error)
            }
            isLoading = false
        }
    }
}
