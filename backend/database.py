import pymysql
from config import Config
from datetime import datetime

class Database:
    """Database connection and operations handler"""
    
    def __init__(self):
        self.config = Config()
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = pymysql.connect(
                host=self.config.DB_HOST,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                database=self.config.DB_NAME,
                port=self.config.DB_PORT,
                cursorclass=pymysql.cursors.DictCursor
            )
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def insert_complaint(self, sender_email, subject, body, priority, category='General'):
        """Insert a new complaint into database"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO complaints 
                (sender_email, subject, body, priority, category, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    sender_email, 
                    subject, 
                    body, 
                    priority, 
                    category,
                    'Pending',
                    datetime.now()
                ))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error inserting complaint: {e}")
            return None
    
    def get_all_complaints(self, limit=100, offset=0):
        """Retrieve all complaints with pagination"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT * FROM complaints 
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
                """
                cursor.execute(sql, (limit, offset))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching complaints: {e}")
            return []
    
    def get_complaint_by_id(self, complaint_id):
        """Get a specific complaint by ID"""
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM complaints WHERE id = %s"
                cursor.execute(sql, (complaint_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching complaint: {e}")
            return None
    
    def update_complaint_status(self, complaint_id, status):
        """Update complaint status"""
        try:
            if not self.connection:
                print("No database connection available")
                return False
                
            with self.connection.cursor() as cursor:
                sql = """
                UPDATE complaints 
                SET status = %s, updated_at = %s 
                WHERE id = %s
                """
                cursor.execute(sql, (status, datetime.now(), complaint_id))
                self.connection.commit()
                affected_rows = cursor.rowcount
                print(f"Updated complaint {complaint_id} to status '{status}'. Rows affected: {affected_rows}")
                return affected_rows > 0
        except Exception as e:
            print(f"Error updating status: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def get_complaints_by_priority(self, priority):
        """Get complaints filtered by priority"""
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM complaints WHERE priority = %s ORDER BY created_at DESC"
                cursor.execute(sql, (priority,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching complaints by priority: {e}")
            return []
    
    def get_complaints_by_status(self, status):
        """Get complaints filtered by status"""
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM complaints WHERE status = %s ORDER BY created_at DESC"
                cursor.execute(sql, (status,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching complaints by status: {e}")
            return []
    
    def search_complaints(self, query):
        """Search complaints by email, subject, or body"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT * FROM complaints 
                WHERE sender_email LIKE %s 
                   OR subject LIKE %s 
                   OR body LIKE %s
                ORDER BY created_at DESC
                """
                search_term = f"%{query}%"
                cursor.execute(sql, (search_term, search_term, search_term))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error searching complaints: {e}")
            return []
    
    def get_statistics(self):
        """Get dashboard statistics"""
        try:
            with self.connection.cursor() as cursor:
                stats = {}
                
                # Total complaints
                cursor.execute("SELECT COUNT(*) as total FROM complaints")
                stats['total'] = cursor.fetchone()['total']
                
                # By priority
                cursor.execute("""
                    SELECT priority, COUNT(*) as count 
                    FROM complaints 
                    GROUP BY priority
                """)
                priority_stats = cursor.fetchall()
                stats['by_priority'] = {item['priority']: item['count'] for item in priority_stats}
                
                # By status
                cursor.execute("""
                    SELECT status, COUNT(*) as count 
                    FROM complaints 
                    GROUP BY status
                """)
                status_stats = cursor.fetchall()
                stats['by_status'] = {item['status']: item['count'] for item in status_stats}
                
                return stats
        except Exception as e:
            print(f"Error fetching statistics: {e}")
            return {}
    
    def check_duplicate_complaint(self, sender_email, subject, hours=24):
        """Check if similar complaint exists within time window"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT * FROM complaints 
                WHERE sender_email = %s 
                  AND subject = %s 
                  AND created_at >= DATE_SUB(NOW(), INTERVAL %s HOUR)
                """
                cursor.execute(sql, (sender_email, subject, hours))
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking duplicate: {e}")
            return False
