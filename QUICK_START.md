# ⚡ Quick Start Guide

## 🎯 Goal
Get the Complaint Priority Management System running in **10 minutes**!

---

## ✅ Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] MySQL installed and running
- [ ] Gmail account with App Password

---

## 🚀 Setup Steps

### 1️⃣ Database Setup (2 minutes)

```bash
# Start MySQL (Windows)
# MySQL should be running as a service

# Create database
mysql -u root -p
CREATE DATABASE complaint_system;
EXIT;
```

### 2️⃣ Backend Setup (3 minutes)

```bash
# Navigate to backend
cd "c:\Users\buvan\OneDrive\Documents\Complaint Priority Management System\backend"

# Create virtual environment
python -m venv venv

# Activate (PowerShell)
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your credentials (email, database password)

# Initialize database
python init_db.py

# Start server
python app.py
```

**Backend ready at:** http://localhost:5000 ✅

### 3️⃣ Frontend Setup (3 minutes)

**Open NEW terminal window**

```bash
# Navigate to frontend
cd "c:\Users\buvan\OneDrive\Documents\Complaint Priority Management System\frontend"

# Install dependencies
npm install

# Start development server
npm start
```

**Dashboard opens at:** http://localhost:3000 ✅

---

## 🧪 Test the System (2 minutes)

### Option 1: Use Sample Data
If you inserted sample data during `init_db.py`, refresh the dashboard!

### Option 2: Send Test Email

1. **Send email to your configured Gmail:**
   - To: `your-email@gmail.com`
   - Subject: `Fire in Building A - Emergency!`
   - Body: `There is a fire on the 3rd floor. No power supply. Help immediately!`

2. **Wait 60 seconds** (or click "Fetch Emails" button)

3. **Check dashboard** - complaint should appear with **HIGH priority** 🔴

---

## 🎨 Dashboard Features

### Stats Overview
- Total complaints count
- High/Medium/Low priority counts
- Pending/Resolved status counts

### Filters
- 🔍 **Search:** Find complaints by email/subject/body
- 📊 **Priority:** Filter by High/Medium/Low
- 📋 **Status:** Filter by Pending/In Progress/Resolved

### Actions
- 👁️ **View:** See full complaint details
- ✏️ **Update Status:** Change status and notify customer
- 📧 **Fetch Emails:** Manually trigger email check

---

## 🔑 Important Files to Configure

### Backend: `.env`
```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
DB_PASSWORD=your_mysql_password
```

### How to Get Gmail App Password:
1. Google Account → Security
2. Enable 2-Step Verification
3. Security → App passwords
4. Generate password for "Mail"
5. Copy 16-character password

---

## 📊 Priority Classification

| Priority | Example Keywords |
|----------|-----------------|
| **🔴 High** | fire, emergency, no power, leak, spark, urgent |
| **🟠 Medium** | slow, not working, broken, wifi issue, problem |
| **🟢 Low** | cleaning, request, inquiry, suggestion |

---

## 🐛 Common Issues

### "Module not found"
```bash
# Ensure venv is activated
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Port already in use"
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "Database connection failed"
- Check MySQL is running
- Verify DB_PASSWORD in `.env`
- Ensure database exists

### "Email authentication failed"
- Use App Password, NOT regular password
- Enable 2-Step Verification first
- Regenerate App Password

---

## 📁 Project Structure

```
Complaint Priority Management System/
│
├── backend/
│   ├── app.py                    # Flask API server
│   ├── email_fetcher.py          # IMAP email fetching
│   ├── priority_classifier.py    # Priority algorithm
│   ├── database.py               # Database operations
│   ├── email_notifier.py         # SMTP notifications
│   ├── config.py                 # Configuration
│   ├── init_db.py                # Database setup
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── App.js                # Main React component
│   │   ├── api.js                # API client
│   │   └── components/
│   │       ├── ComplaintModal.js # Detail modal
│   │       └── StatsCards.js     # Statistics cards
│   ├── package.json              # Node dependencies
│   └── public/
│
├── README.md                     # Project overview
├── SETUP_GUIDE.md               # Detailed setup
├── API_DOCUMENTATION.md         # API reference
└── PRIORITY_ALGORITHM.md        # Algorithm details
```

---

## 🎯 What's Next?

### Immediate Testing
1. ✅ Send test emails with different priorities
2. ✅ Update complaint statuses
3. ✅ Test email notifications
4. ✅ Try search and filters

### Customization
- Add custom priority keywords
- Create new categories
- Adjust fetch interval
- Customize email templates

### Production Deployment
- Set up on cloud server (AWS, Azure, DigitalOcean)
- Configure HTTPS
- Add authentication
- Set up monitoring

---

## 💡 Pro Tips

1. **Auto-refresh:** Dashboard refreshes every 30 seconds
2. **Background fetch:** Emails checked every 60 seconds (configurable)
3. **Duplicate prevention:** Same subject from same sender within 24h = skipped
4. **Priority explanation:** Check backend console for classification reasons
5. **Notifications:** Optional email sent to customer on status update

---

## 📞 Quick Commands

```bash
# Start backend
cd backend
venv\Scripts\Activate.ps1
python app.py

# Start frontend (new terminal)
cd frontend
npm start

# Initialize database
cd backend
python init_db.py

# Test email fetcher
cd backend
python email_fetcher.py
```

---

## ✨ Success Indicators

✅ Backend console shows: "Running on http://0.0.0.0:5000"  
✅ Frontend opens in browser automatically  
✅ Dashboard displays stats cards  
✅ No red errors in browser console  
✅ Email fetch button works  
✅ Complaints appear in table  

---

## 🎉 You're All Set!

Your intelligent complaint management system is now operational!

**Features Working:**
- ✅ Automatic email fetching
- ✅ Smart priority classification
- ✅ Real-time dashboard
- ✅ Status management
- ✅ Email notifications
- ✅ Search & filters

**Enjoy managing complaints efficiently!** 🚀

---

**Need detailed help?** Check `SETUP_GUIDE.md` for comprehensive instructions!
