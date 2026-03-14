import SwiftUI

// FBA website brand color: #A85D21
extension Color {
    static let saffronOrange = Color(red: 168/255, green: 93/255, blue: 33/255)  // #A85D21
    static let deepSaffron = Color(red: 126/255, green: 69/255, blue: 24/255)    // #7E4518
    static let warmGold = Color(red: 196/255, green: 122/255, blue: 58/255)      // #C47A3A
    static let darkBrown = Color(red: 62/255, green: 39/255, blue: 35/255)       // #3E2723
}

extension ShapeStyle where Self == Color {
    static var fbaAccent: Color { .saffronOrange }
}
