# 🚀 Complaint Priority Management System - Setup Guide

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 14+** ([Download](https://nodejs.org/))
- **MySQL 8.0+** ([Download](https://dev.mysql.com/downloads/mysql/))
- **Gmail Account** with App Password enabled

---

## 📧 Gmail Configuration (Required)

### Enable Gmail App Password

1. Go to your Google Account settings
2. Navigate to **Security** > **2-Step Verification** (enable if not already)
3. Go to **Security** > **App passwords**
4. Select **Mail** and **Windows Computer** (or Other)
5. Generate password and **save it securely**

**Important:** Use the generated app password, NOT your regular Gmail password!

---

## ⚙️ Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd "c:\Users\buvan\OneDrive\Documents\Complaint Priority Management System\backend"
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

1. Copy the example file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file with your actual credentials:
   ```env
   # Email Configuration
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your_app_password_here
   IMAP_SERVER=imap.gmail.com
   IMAP_PORT=993
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587

   # Database Configuration
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=complaint_system
   DB_PORT=3306

   # Flask Configuration
   FLASK_ENV=development
   SECRET_KEY=your_random_secret_key_here
   FLASK_DEBUG=True

   # CORS
   CORS_ORIGINS=http://localhost:3000

   # Email Fetch Interval (in seconds)
   EMAIL_FETCH_INTERVAL=60
   ```

### Step 6: Set Up MySQL Database

1. **Start MySQL Server**

2. **Run Database Initialization:**
   ```bash
   python init_db.py
   ```

   This will:
   - Create the `complaint_system` database
   - Create required tables
   - (Optional) Insert sample data for testing

### Step 7: Start Backend Server

```bash
python app.py
```

**Expected Output:**
```
================================================================
🚀 Complaint Priority Management System - Backend API
================================================================
📧 Email monitoring: your-email@gmail.com
⏱️  Fetch interval: 60 seconds
🗄️  Database: complaint_system
🌐 CORS enabled for: http://localhost:3000
================================================================

 * Running on http://0.0.0.0:5000
```

Backend is now running at: **http://localhost:5000**

---

## 🎨 Frontend Setup

### Step 1: Open New Terminal

Keep the backend running and open a **new terminal window**.

### Step 2: Navigate to Frontend Directory

```bash
cd "c:\Users\buvan\OneDrive\Documents\Complaint Priority Management System\frontend"
```

### Step 3: Install Dependencies

```bash
npm install
```

### Step 4: (Optional) Configure API URL

If your backend is on a different port/host, create `.env` file:

```bash
copy .env.example .env
```

Edit if needed (default is fine for local development):
```env
REACT_APP_API_URL=http://localhost:5000/api
```

### Step 5: Start Frontend Server

```bash
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view complaint-dashboard in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

Your browser will automatically open to: **http://localhost:3000**

---

## ✅ Verify Installation

### 1. Check Backend Health

Open browser: http://localhost:5000/api/health

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-08T...",
  "scheduler_running": true
}
```

### 2. Check Frontend

Dashboard should display:
- Statistics cards
- Email fetch button
- Filter controls
- Complaints table (may be empty initially)

### 3. Test Email Fetching

1. Send a test email to your configured Gmail address
2. Subject: "Test Complaint - No Power"
3. Body: "There is no electricity in building A. This is urgent!"
4. Wait 60 seconds (or click "Fetch Emails" button in dashboard)
5. Complaint should appear in the dashboard with **High Priority**

---

## 🔧 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Access denied for user 'root'@'localhost'"

**Solution:**
- Check MySQL username/password in `.env` file
- Ensure MySQL server is running
- Test connection: `mysql -u root -p`

### Issue: "Authentication failed" (Email)

**Solution:**
- Make sure you're using **App Password**, not regular password
- Enable 2-Step Verification in Google Account
- Generate new App Password
- Update `EMAIL_PASSWORD` in `.env`

### Issue: Port 5000 or 3000 already in use

**Solution (PowerShell):**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Issue: CORS errors in browser console

**Solution:**
- Ensure backend is running
- Check `CORS_ORIGINS` in backend `.env` matches frontend URL
- Restart backend server

---

## 📊 Using the System

### Admin Dashboard Features

1. **View Complaints**
   - All complaints displayed in table
   - Color-coded priority badges
   - Status indicators

2. **Filter & Search**
   - Filter by priority (High/Medium/Low)
   - Filter by status (Pending/In Progress/Resolved)
   - Search by email, subject, or body

3. **Update Status**
   - Click "View" on any complaint
   - Modal shows full details
   - Change status and optionally send email notification
   - Click "Update Status"

4. **Manual Email Fetch**
   - Click "📧 Fetch Emails" button
   - Manually triggers email check
   - Bypasses scheduled interval

5. **Auto-Refresh**
   - Dashboard auto-refreshes every 30 seconds
   - Background email fetching every 60 seconds (configurable)

### Priority Classification Examples

**High Priority (Red):**
- "Fire in the building!"
- "No power supply - spark detected"
- "Water leakage emergency"

**Medium Priority (Orange):**
- "WiFi not working in my room"
- "Internet speed is very slow"
- "Printer is broken"

**Low Priority (Green):**
- "Need room cleaning tomorrow"
- "General inquiry about facilities"
- "Suggestion for improvement"

---

## 🛠️ Advanced Configuration

### Change Email Fetch Interval

Edit `backend\.env`:
```env
EMAIL_FETCH_INTERVAL=30  # Check every 30 seconds
```

### Add Custom Priority Keywords

Edit `backend\priority_classifier.py`:
```python
self.high_priority_keywords = [
    'fire', 'emergency', 'urgent',
    'your_custom_keyword_here'  # Add your keywords
]
```

### Customize Categories

Edit `backend\priority_classifier.py` in `get_category()` method:
```python
categories = {
    'Your Category': ['keyword1', 'keyword2'],
    # Add more categories...
}
```

---

## 📝 API Documentation

### Get All Complaints
```
GET /api/complaints
Query Params: priority, status, search, limit, offset
```

### Get Single Complaint
```
GET /api/complaints/<id>
```

### Update Complaint Status
```
PUT /api/complaints/<id>
Body: { "status": "In Progress", "send_notification": true }
```

### Get Statistics
```
GET /api/stats
```

### Fetch Emails Manually
```
POST /api/fetch-emails
```

---

## 🔐 Security Recommendations

**For Production Deployment:**

1. **Change Secret Key:**
   ```env
   SECRET_KEY=generate_a_strong_random_key_here
   ```

2. **Use Environment Variables:**
   - Never commit `.env` file to git
   - Use secure secret management

3. **Database Security:**
   - Create dedicated MySQL user (not root)
   - Use strong passwords
   - Limit privileges

4. **HTTPS:**
   - Use HTTPS for production
   - Configure SSL certificates

5. **Rate Limiting:**
   - Add rate limiting to API endpoints
   - Prevent abuse

---

## 📞 Troubleshooting

### Enable Debug Logging

Backend:
```python
# In app.py
app.config['DEBUG'] = True
```

### Check Email Connection

Run standalone test:
```bash
cd backend
python email_fetcher.py
```

### Database Connection Test

```bash
python -c "from database import Database; db = Database(); print(db.connect())"
```

---

## 🎉 Success!

If everything is working:
- ✅ Backend running on port 5000
- ✅ Frontend running on port 3000
- ✅ MySQL database connected
- ✅ Email fetching active
- ✅ Dashboard displays complaints

**Congratulations!** Your Complaint Priority Management System is now operational! 🚀

---

## 📚 Next Steps

- Customize priority keywords
- Add more categories
- Implement user authentication
- Deploy to production server
- Add analytics dashboard
- Integrate machine learning

---

## 💡 Tips

- Monitor backend console for email fetch logs
- Check browser console for any frontend errors
- Use sample data to test the system initially
- Send test emails to verify priority classification
- Experiment with different keywords

---

**Need Help?** Check the logs, verify configurations, and ensure all services are running!
