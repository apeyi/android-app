import XCTest
@testable import FBAudio

final class HelpersTests: XCTestCase {

    func testFormatDurationMinutesSeconds() {
        XCTAssertEqual(formatDuration(0), "0:00")
        XCTAssertEqual(formatDuration(65), "1:05")
        XCTAssertEqual(formatDuration(600), "10:00")
    }

    func testFormatDurationHours() {
        XCTAssertEqual(formatDuration(3600), "1:00:00")
        XCTAssertEqual(formatDuration(3661), "1:01:01")
        XCTAssertEqual(formatDuration(7200), "2:00:00")
    }

    func testFormatFileSize() {
        XCTAssertEqual(formatFileSize(0), "")
        XCTAssertEqual(formatFileSize(512), "512 B")
        XCTAssertTrue(formatFileSize(1500).contains("KB"))
        XCTAssertTrue(formatFileSize(1_500_000).contains("MB"))
        XCTAssertTrue(formatFileSize(1_500_000_000).contains("GB"))
    }
}
