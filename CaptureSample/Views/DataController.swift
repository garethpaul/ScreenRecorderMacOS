//
//  DataController.swift
//  CaptureSample
//
//  Created by gpj on 11/24/22.
//  Copyright © 2022 Apple. All rights reserved.
//

import CoreData
import Foundation
import OSLog

class DataController:  ObservableObject  {
    let container = NSPersistentContainer(name: "Video")
    private let logger = Logger()

    static var shared = DataController()

    init() {
        container.loadPersistentStores { description, error in
            if let error = error {
                self.logger.error("Core Data failed to load: \(error.localizedDescription)")
            }
        }
    }

    var moc: NSManagedObjectContext {
        return (container.viewContext)
    }

    //Save context, if changes were made
        func save() {
            if moc.hasChanges {
                do {
                    try moc.save()
                } catch {
                    logger.error("Error while saving managedObjectContext: \(String(describing: error))")
                }
            }
        }


    

    
}
public extension NSManagedObject {

    convenience init(usedContext: NSManagedObjectContext) {
        let name = String(describing: type(of: self))
        let entity = NSEntityDescription.entity(forEntityName: name, in: usedContext)!
        self.init(entity: entity, insertInto: usedContext)
    }

}
