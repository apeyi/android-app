import Foundation

enum CategoryType: String {
    case sangharakshita
    case mitraStudy
    case mitraYear
    case mitraModule
    case theme
    case year
    case series
}

struct BrowseCategory: Identifiable {
    let id: String
    let name: String
    let type: CategoryType
    let browseUrl: String
}
