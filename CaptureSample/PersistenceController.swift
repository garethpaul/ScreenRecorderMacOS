//
//  PersistenceController.swift
//  CaptureSample
//
//  Created by gpj on 11/24/22.
//  Copyright © 2022 Apple. All rights reserved.
//

import Foundation
import CoreData
import OSLog

struct PersistenceController {
    // A singleton for our entire app to use
    static let shared = PersistenceController()
    private let logger = Logger()

    // Storage for Core Data
    let container: NSPersistentContainer

    // A test configuration for SwiftUI previews
    static var preview: PersistenceController = {
        let controller = PersistenceController(inMemory: true)

        return controller
    }()

    // An initializer to load Core Data, optionally able
    // to use an in-memory store.
    init(inMemory: Bool = false) {
        container = NSPersistentContainer(name: "Video")

        if inMemory {
            container.persistentStoreDescriptions.first?.url = URL(fileURLWithPath: "/dev/null")
        }

        let logger = self.logger
        container.loadPersistentStores { description, error in
            if let error = error {
                logger.error("Core Data failed to load: \(error.localizedDescription)")
            }
        }
    }
}
