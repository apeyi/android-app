import Foundation

struct Talk: Identifiable, Codable, Equatable {
    let catNum: String
    let title: String
    let speaker: String
    let year: Int
    let genre: String
    let durationSeconds: Int
    let imageUrl: String
    let audioUrl: String
    let description: String
    var tracks: [Track]
    let transcriptUrl: String
    let series: String
    let seriesHref: String

    var id: String { catNum }

    init(catNum: String, title: String = "", speaker: String = "", year: Int = 0,
         genre: String = "", durationSeconds: Int = 0, imageUrl: String = "",
         audioUrl: String = "", description: String = "", tracks: [Track] = [],
         transcriptUrl: String = "", series: String = "", seriesHref: String = "") {
        self.catNum = catNum
        self.title = title
        self.speaker = speaker
        self.year = year
        self.genre = genre
        self.durationSeconds = durationSeconds
        self.imageUrl = imageUrl
        self.audioUrl = audioUrl
        self.description = description
        self.tracks = tracks
        self.transcriptUrl = transcriptUrl
        self.series = series
        self.seriesHref = seriesHref
    }
}

struct Track: Codable, Equatable {
    let title: String
    let durationSeconds: Int
    let audioUrl: String
}
