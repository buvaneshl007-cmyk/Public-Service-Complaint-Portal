from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from database import Database
from email_fetcher import EmailFetcher
from email_notifier import EmailNotifier
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit
import os

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}}, supports_credentials=True)

# Initialize components
db = Database()
email_fetcher = EmailFetcher()
email_notifier = EmailNotifier()

# Background scheduler for automatic email fetching
scheduler = BackgroundScheduler()

def fetch_emails_job():
    """Background job to fetch emails automatically"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running scheduled email fetch...")
    result = email_fetcher.process_and_store_emails()
    print(f"Result: {result}")

# Schedule email fetching every N seconds (configurable)
scheduler.add_job(
    func=fetch_emails_job,
    trigger="interval",
    seconds=Config.EMAIL_FETCH_INTERVAL,
    id='email_fetch_job',
    name='Fetch emails periodically',
    replace_existing=True
)

# Start scheduler
scheduler.start()

# Shutdown scheduler when app exits
atexit.register(lambda: scheduler.shutdown())


# ============= API ROUTES =============

@app.route('/')
def index():
    """Serve the HTML dashboard"""
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return send_from_directory(parent_dir, 'dashboard.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "scheduler_running": scheduler.running
    })


@app.route('/api/complaints', methods=['GET'])
def get_complaints():
    """Get all complaints with optional filters"""
    try:
        # Connect to database
        if not db.connect():
            return jsonify({"error": "Database connection failed"}), 500
        
        # Get query parameters
        priority = request.args.get('priority')
        status = request.args.get('status')
        search = request.args.get('search')
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        
        # Apply filters
        if search:
            complaints = db.search_complaints(search)
        elif priority:
            complaints = db.get_complaints_by_priority(priority)
        elif status:
            complaints = db.get_complaints_by_status(status)
        else:
            complaints = db.get_all_complaints(limit, offset)
        
        db.close()
        
        # Convert datetime objects to strings
        for complaint in complaints:
            if complaint.get('created_at'):
                complaint['created_at'] = complaint['created_at'].isoformat()
            if complaint.get('updated_at'):
                complaint['updated_at'] = complaint['updated_at'].isoformat()
        
        return jsonify({
            "success": True,
            "count": len(complaints),
            "complaints": complaints
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/complaints/<int:complaint_id>', methods=['GET'])
def get_complaint(complaint_id):
    """Get a specific complaint by ID"""
    try:
        if not db.connect():
            return jsonify({"error": "Database connection failed"}), 500
        
        complaint = db.get_complaint_by_id(complaint_id)
        db.close()
        
        if not complaint:
            return jsonify({"error": "Complaint not found"}), 404
        
        # Convert datetime to string
        if complaint.get('created_at'):
            complaint['created_at'] = complaint['created_at'].isoformat()
        if complaint.get('updated_at'):
            complaint['updated_at'] = complaint['updated_at'].isoformat()
        
        return jsonify({
            "success": True,
            "complaint": complaint
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/complaints/<int:complaint_id>', methods=['PUT'])
def update_complaint(complaint_id):
    """Update complaint status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({"error": "Status is required"}), 400
        
        valid_statuses = ['Pending', 'In Progress', 'Resolved', 'Closed', 'Rejected']
        if new_status not in valid_statuses:
            return jsonify({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400
        
        if not db.connect():
            return jsonify({"error": "Database connection failed"}), 500
        
        # Get old status for notification
        old_complaint = db.get_complaint_by_id(complaint_id)
        if not old_complaint:
            db.close()
            return jsonify({"error": "Complaint not found"}), 404
        
        old_status = old_complaint['status']
        
        # Update status
        success = db.update_complaint_status(complaint_id, new_status)
        db.close()
        
        if not success:
            return jsonify({"error": "Failed to update status"}), 500
        
        # Send notification if requested
        send_notification = data.get('send_notification', False)
        if send_notification and old_status != new_status:
            if new_status == 'Resolved':
                email_notifier.send_complaint_resolved(
                    old_complaint['sender_email'],
                    complaint_id,
                    old_complaint['subject']
                )
            else:
                email_notifier.send_status_update(
                    old_complaint['sender_email'],
                    complaint_id,
                    old_complaint['subject'],
                    old_status,
                    new_status
                )
        
        return jsonify({
            "success": True,
            "message": "Status updated successfully",
            "old_status": old_status,
            "new_status": new_status
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get dashboard statistics"""
    try:
        if not db.connect():
            return jsonify({"error": "Database connection failed"}), 500
        
        stats = db.get_statistics()
        db.close()
        
        return jsonify({
            "success": True,
            "stats": stats
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/fetch-emails', methods=['POST'])
def manual_fetch_emails():
    """Manually trigger email fetching"""
    try:
        result = email_fetcher.process_and_store_emails()
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/test-notification', methods=['POST'])
def test_notification():
    """Test email notification"""
    try:
        data = request.get_json()
        to_email = data.get('email')
        
        if not to_email:
            return jsonify({"error": "Email address is required"}), 400
        
        success = email_notifier.send_notification(
            to_email,
            "Test Notification",
            "This is a test notification from the Complaint Management System.",
            None
        )
        
        return jsonify({
            "success": success,
            "message": "Test email sent" if success else "Failed to send test email"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# Run application
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏙️ CityCare - Backend API")
    print("="*60)
    print(f"📧 Email monitoring: {Config.EMAIL_ADDRESS}")
    print(f"⏱️  Fetch interval: {Config.EMAIL_FETCH_INTERVAL} seconds")
    print(f"🗄️  Database: {Config.DB_NAME}")
    print(f"🌐 CORS enabled for: {', '.join(Config.CORS_ORIGINS)}")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )
