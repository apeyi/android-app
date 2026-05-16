import XCTest
@testable import FBAudio

final class SharedDataLoaderTests: XCTestCase {

    func testSangharakshitaTalksLoaded() {
        let talks = SharedDataLoader.sangharakshitaTalks
        XCTAssertGreaterThan(talks.count, 300, "Should have 300+ Sangharakshita talks")
    }

    func testSangharakshitaSeriesLoaded() {
        let series = SharedDataLoader.sangharakshitaSeries
        XCTAssertGreaterThan(series.count, 20, "Should have 20+ series")
    }

    func testTitleFixing() {
        let talks = SharedDataLoader.sangharakshitaTalks
        // No talk title should end with ", The" / ", A" / ", An"
        for talk in talks {
            XCTAssertFalse(talk.title.hasSuffix(", The"), "Title not fixed: \(talk.title)")
            XCTAssertFalse(talk.title.hasSuffix(", A"), "Title not fixed: \(talk.title)")
            XCTAssertFalse(talk.title.hasSuffix(", An"), "Title not fixed: \(talk.title)")
        }
    }

    func testSangharakshitaSeriesCategories() {
        let categories = SharedDataLoader.sangharakshitaSeriesAsCategories()
        XCTAssertGreaterThan(categories.count, 0)
        XCTAssertTrue(categories.allSatisfy { $0.type == .series })
        XCTAssertTrue(categories.allSatisfy { $0.browseUrl.contains("/series/details") })
    }

}
