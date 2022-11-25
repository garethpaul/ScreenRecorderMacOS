//
//  DataController.swift
//  CaptureSample
//
//  Created by gpj on 11/24/22.
//  Copyright © 2022 Apple. All rights reserved.
//

import CoreData
import Foundation

class DataController:  ObservableObject  {
    let container = NSPersistentContainer(name: "Video")

    static var shared = DataController()

    init() {
        container.loadPersistentStores { description, error in
            if let error = error {
                print("Core Data failed to load \(error.localizedDescription)")
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
                    print("Sucess!!")
                    try moc.save()
                } catch {
                    print("Error while saving managedObjectContext \(error)")
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
