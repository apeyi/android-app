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

    func testMitraModulesLoaded() {
        let modules = SharedDataLoader.mitraModules
        XCTAssertGreaterThan(modules.count, 20, "Should have 20+ Mitra Study modules")
    }

    func testMitraModulesByYear() {
        let grouped = SharedDataLoader.modulesByYear()
        XCTAssertEqual(Set(grouped.keys), [1, 2, 3, 4], "Should have years 1-4")
        for (_, modules) in grouped {
            XCTAssertGreaterThan(modules.count, 0)
        }
    }

    func testMitraModuleTalks() {
        let talks = SharedDataLoader.moduleTalksAsSearchResults("y1_refuge")
        XCTAssertGreaterThan(talks.count, 0, "y1_refuge module should have talks")
        XCTAssertTrue(talks.allSatisfy { !$0.catNum.isEmpty })
    }

    func testMitraYearCategories() {
        let categories = SharedDataLoader.yearCategories()
        XCTAssertEqual(categories.count, 4)
        XCTAssertEqual(categories.map(\.name), ["Year 1", "Year 2", "Year 3", "Year 4"])
    }
}
