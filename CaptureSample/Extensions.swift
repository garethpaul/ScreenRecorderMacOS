import Foundation

extension Date {
    func passedTime(from date: Date) -> String {
        let difference = Calendar.current.dateComponents([.minute, .second], from: date, to: self)

        let strMin = String(format: "%02d", difference.minute ?? 00)
        let strSec = String(format: "%02d", difference.second ?? 00)

        return "\(strMin):\(strSec)"
    }
}
