"""
Database Initialization Script
Run this script to set up the MySQL database and tables
"""

import pymysql
from config import Config

def init_database():
    """Initialize database and create tables"""
    config = Config()
    
    print("="*60)
    print("Database Initialization")
    print("="*60)
    
    try:
        # Connect to MySQL server (without database)
        connection = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT
        )
        
        cursor = connection.cursor()
        
        # Create database
        print(f"Creating database: {config.DB_NAME}")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}")
        print("✓ Database created/verified")
        
        # Use database
        cursor.execute(f"USE {config.DB_NAME}")
        
        # Create complaints table
        print("\nCreating complaints table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender_email VARCHAR(255) NOT NULL,
                subject VARCHAR(500) NOT NULL,
                body TEXT NOT NULL,
                priority ENUM('High', 'Medium', 'Low') NOT NULL DEFAULT 'Low',
                category VARCHAR(100) DEFAULT 'General',
                status ENUM('Pending', 'In Progress', 'Resolved', 'Closed', 'Rejected') NOT NULL DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                
                INDEX idx_priority (priority),
                INDEX idx_status (status),
                INDEX idx_sender_email (sender_email),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Complaints table created/verified")
        
        # Create admin_actions table
        print("\nCreating admin_actions table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_actions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                complaint_id INT NOT NULL,
                action_type VARCHAR(50) NOT NULL,
                old_value VARCHAR(100),
                new_value VARCHAR(100),
                admin_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE,
                INDEX idx_complaint_id (complaint_id),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Admin actions table created/verified")
        
        connection.commit()
        
        # Insert sample data (optional)
        print("\n" + "="*60)
        insert_sample = input("Insert sample data for testing? (y/n): ").lower()
        
        if insert_sample == 'y':
            print("\nInserting sample data...")
            cursor.execute("""
                INSERT INTO complaints (sender_email, subject, body, priority, category, status) VALUES
                ('user1@example.com', 'No power in Block B', 'There is no electricity in our hostel block. This is urgent! Fire hazard!', 'High', 'Electrical', 'Pending'),
                ('user2@example.com', 'Slow internet connection', 'The wifi speed is very slow in my room. Please fix it.', 'Medium', 'Network/IT', 'In Progress'),
                ('user3@example.com', 'Room cleaning request', 'Need cleaning service for my room tomorrow.', 'Low', 'Cleaning', 'Pending'),
                ('user4@example.com', 'Water leakage in bathroom', 'There is water leaking from the ceiling. Emergency!', 'High', 'Plumbing', 'Pending'),
                ('user5@example.com', 'AC not working', 'The air conditioning unit is not cooling properly.', 'Medium', 'HVAC', 'Pending')
            """)
            connection.commit()
            print("✓ Sample data inserted")
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*60)
        print("✓ Database initialization completed successfully!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        return False

if __name__ == "__main__":
    init_database()
