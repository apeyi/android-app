import Foundation

struct SearchResult: Identifiable, Equatable {
    let catNum: String
    let title: String
    let speaker: String
    let imageUrl: String
    let path: String
    let year: Int

    var id: String { catNum }

    init(catNum: String, title: String = "", speaker: String = "",
         imageUrl: String = "", path: String = "", year: Int = 0) {
        self.catNum = catNum
        self.title = title
        self.speaker = speaker
        self.imageUrl = imageUrl
        self.path = path
        self.year = year
    }
}
