import Foundation
import SwiftSoup

enum TranscriptParser {

    static func parseTranscriptHtml(_ html: String) -> String {
        if let content = extractFbaTextContent(html) {
            let text = contentToPlainText(content)
            if !text.isEmpty { return text }
        }
        // Fallback
        guard let doc = try? SwiftSoup.parse(html) else { return "" }
        let selectors = [".text-content", ".content", "article", "main"]
        for selector in selectors {
            if let el = try? doc.select(selector).first(), let text = try? el.text(), !text.isEmpty {
                return text
            }
        }
        return (try? doc.body()?.text()) ?? ""
    }

    private static func extractFbaTextContent(_ html: String) -> String? {
        guard let doc = try? SwiftSoup.parse(html) else { return nil }
        guard let scripts = try? doc.select("script") else { return nil }
        for script in scripts {
            let data = (try? script.data()) ?? ""
            let marker = "document.__FBA__.text"
            guard let idx = data.range(of: marker) else { continue }
            let rest = data[idx.upperBound...]
            guard let braceIdx = rest.firstIndex(of: "{") else { continue }
            guard let jsonStr = extractBalancedBraces(String(rest[braceIdx...])) else { continue }
            guard let jsonData = jsonStr.data(using: .utf8),
                  let json = try? JSONSerialization.jsonObject(with: jsonData) as? [String: Any],
                  let content = json["content"] as? String else { continue }
            return content
        }
        return nil
    }

    static func contentToPlainText(_ content: String) -> String {
        guard !content.isEmpty, let doc = try? SwiftSoup.parse(content) else { return "" }
        doc.outputSettings().prettyPrint(pretty: false)
        let selectors = "p, br, h1, h2, h3, h4, h5, h6, blockquote, li"
        guard let elements = try? doc.select(selectors) else {
            return (try? doc.text())?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
        }
        var sb = ""
        for el in elements {
            let text = (try? el.text())?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
            if !text.isEmpty {
                sb += text + "\n\n"
            }
        }
        if !sb.isEmpty { return sb.trimmingCharacters(in: .whitespacesAndNewlines) }
        return (try? doc.text())?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
    }

    private static func extractBalancedBraces(_ data: String) -> String? {
        var depth = 0
        var inString = false
        var escape = false
        let chars = Array(data)
        for i in 0..<chars.count {
            let c = chars[i]
            if escape { escape = false; continue }
            if c == "\\" && inString { escape = true; continue }
            if c == "\"" { inString = !inString; continue }
            if !inString {
                if c == "{" { depth += 1 }
                else if c == "}" {
                    depth -= 1
                    if depth == 0 { return String(chars[0...i]) }
                }
            }
        }
        return nil
    }
}
