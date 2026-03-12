import SwiftUI

extension Color {
    static let saffronOrange = Color(red: 232/255, green: 137/255, blue: 29/255)
    static let deepSaffron = Color(red: 197/255, green: 113/255, blue: 26/255)
    static let warmGold = Color(red: 245/255, green: 200/255, blue: 66/255)
    static let darkBrown = Color(red: 62/255, green: 39/255, blue: 35/255)
    static let cream = Color(red: 255/255, green: 248/255, blue: 225/255)
}

extension ShapeStyle where Self == Color {
    static var fbaAccent: Color { .saffronOrange }
}
