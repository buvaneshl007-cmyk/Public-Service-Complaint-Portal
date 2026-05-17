"""
Script to reclassify all existing complaints with the updated priority logic
This will update complaints that were classified with the old keyword-only logic
"""

from database import Database
from priority_classifier import PriorityClassifier

def reclassify_all_complaints():
    """Reclassify all complaints in the database"""
    
    db = Database()
    classifier = PriorityClassifier()
    
    print("="*60)
    print("Reclassifying All Complaints with Updated Logic")
    print("="*60)
    
    try:
        # Connect to database
        if not db.connect():
            print("❌ Failed to connect to database")
            return
        
        # Get all complaints
        complaints = db.get_all_complaints(limit=1000)
        
        if not complaints:
            print("No complaints found in database")
            db.close()
            return
        
        print(f"\nFound {len(complaints)} complaint(s) to reclassify\n")
        
        updated_count = 0
        
        for complaint in complaints:
            complaint_id = complaint['id']
            old_priority = complaint['priority']
            
            # Combine subject and body for classification
            full_text = f"{complaint['subject']} {complaint['body']}"
            
            # Reclassify with new logic
            new_priority = classifier.classify(full_text)
            new_category = classifier.get_category(full_text)
            
            # Update if priority changed
            if old_priority != new_priority:
                # Update in database
                cursor = db.connection.cursor()
                cursor.execute(
                    "UPDATE complaints SET priority = %s, category = %s WHERE id = %s",
                    (new_priority, new_category, complaint_id)
                )
                db.connection.commit()
                
                print(f"✅ Complaint #{complaint_id}: {old_priority} → {new_priority}")
                print(f"   Subject: {complaint['subject'][:50]}...")
                print(f"   Reason: {classifier.get_priority_explanation(new_priority, full_text)}\n")
                updated_count += 1
            else:
                print(f"⚪ Complaint #{complaint_id}: {old_priority} (no change)")
        
        db.close()
        
        print("="*60)
        print(f"✅ Reclassification Complete!")
        print(f"   Total complaints: {len(complaints)}")
        print(f"   Updated: {updated_count}")
        print(f"   Unchanged: {len(complaints) - updated_count}")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.close()

if __name__ == "__main__":
    reclassify_all_complaints()
