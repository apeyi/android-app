import Foundation

struct BrowsePage {
    let items: [SearchResult]
    let totalItems: Int
    let apiBaseUrl: String
    let browseQueryString: String
    let title: String

    var hasMore: Bool { items.count < totalItems }

    init(items: [SearchResult] = [], totalItems: Int = 0, apiBaseUrl: String = "",
         browseQueryString: String = "", title: String = "") {
        self.items = items
        self.totalItems = totalItems
        self.apiBaseUrl = apiBaseUrl
        self.browseQueryString = browseQueryString
        self.title = title
    }
}
