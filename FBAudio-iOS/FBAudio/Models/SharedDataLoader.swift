import Foundation

/// Loads shared JSON data files bundled from fbaudio-shared/
class SharedDataLoader {

    struct SangharakshitaJSON: Codable {
        let speaker: String
        let talks: [SangTalk]
        let series: [SangSeries]
    }

    struct SangTalk: Codable {
        let catNum: String
        let title: String
        let year: Int
        let imageUrl: String
    }

    struct SangSeries: Codable {
        let id: String
        let title: String
    }

    // MARK: - Sangharakshita

    private static var _sangharakshitaTalks: [SearchResult]?
    private static var _sangharakshitaSeries: [SangSeries]?

    private static func fixTitle(_ title: String) -> String {
        if title.hasSuffix(", The") {
            return "The " + title.dropLast(5)
        } else if title.hasSuffix(", A") {
            return "A " + title.dropLast(3)
        } else if title.hasSuffix(", An") {
            return "An " + title.dropLast(4)
        }
        return title
    }

    private static func loadSangharakshita() {
        guard let url = Bundle.main.url(forResource: "sangharakshita", withExtension: "json", subdirectory: "fbaudio-shared") else {
            print("sangharakshita.json not found in bundle")
            return
        }
        guard let data = try? Data(contentsOf: url),
              let json = try? JSONDecoder().decode(SangharakshitaJSON.self, from: data) else {
            print("Failed to decode sangharakshita.json")
            return
        }
        _sangharakshitaTalks = json.talks.map { talk in
            SearchResult(
                catNum: talk.catNum,
                title: fixTitle(talk.title),
                speaker: "Sangharakshita",
                imageUrl: talk.imageUrl,
                path: "https://www.freebuddhistaudio.com/audio/details?num=\(talk.catNum)",
                year: talk.year
            )
        }
        _sangharakshitaSeries = json.series
    }

    static var sangharakshitaTalks: [SearchResult] {
        if _sangharakshitaTalks == nil { loadSangharakshita() }
        return _sangharakshitaTalks ?? []
    }

    static var sangharakshitaSeries: [SangSeries] {
        if _sangharakshitaSeries == nil { loadSangharakshita() }
        return _sangharakshitaSeries ?? []
    }

    static func sangharakshitaSeriesAsCategories() -> [BrowseCategory] {
        sangharakshitaSeries.map { s in
            BrowseCategory(
                id: "sang_series_\(s.id)",
                name: s.title,
                type: .series,
                browseUrl: "https://www.freebuddhistaudio.com/series/details?num=\(s.id)"
            )
        }
    }

}
