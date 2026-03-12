import XCTest
@testable import FBAudio

final class TranscriptParserTests: XCTestCase {

    func testContentToPlainText() {
        let html = "<p>First paragraph.</p><p>Second paragraph.</p>"
        let result = TranscriptParser.contentToPlainText(html)
        XCTAssertTrue(result.contains("First paragraph."))
        XCTAssertTrue(result.contains("Second paragraph."))
    }

    func testContentToPlainTextWithHeaders() {
        let html = "<h1>Title</h1><p>Content here.</p>"
        let result = TranscriptParser.contentToPlainText(html)
        XCTAssertTrue(result.contains("Title"))
        XCTAssertTrue(result.contains("Content here."))
    }

    func testEmptyContent() {
        XCTAssertEqual(TranscriptParser.contentToPlainText(""), "")
    }

    func testParseTranscriptHtmlFallback() {
        let html = "<html><body><div class=\"content\">Some transcript text</div></body></html>"
        let result = TranscriptParser.parseTranscriptHtml(html)
        XCTAssertTrue(result.contains("Some transcript text"))
    }
}
