# 📋 QUICK REFERENCE CARD

## 🚀 Complaint Priority Management System

---

## ⚡ Quick Commands

### Backend

```bash
# Setup
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configure
copy .env.example .env
# Edit .env with your credentials

# Initialize database
python init_db.py

# Start server
python app.py
```

### Frontend

```bash
# Setup
cd frontend
npm install

# Start
npm start
```

---

## 🔑 Essential Configuration

### .env File (Backend)

```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=16_char_app_password
IMAP_SERVER=imap.gmail.com
SMTP_SERVER=smtp.gmail.com
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=complaint_system
```

### Gmail App Password

1. Google Account → Security
2. Enable 2-Step Verification
3. Security → App passwords
4. Generate for "Mail"
5. Use 16-character password

---

## 🌐 URLs

- **Backend API:** http://localhost:5000
- **Frontend Dashboard:** http://localhost:3000
- **Health Check:** http://localhost:5000/api/health

---

## 📊 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Health check |
| GET | `/api/complaints` | Get all complaints |
| GET | `/api/complaints/<id>` | Get one complaint |
| PUT | `/api/complaints/<id>` | Update status |
| GET | `/api/stats` | Get statistics |
| POST | `/api/fetch-emails` | Fetch emails manually |

---

## 🎯 Priority Keywords

### High Priority
fire, emergency, urgent, no power, leak, spark, burst, danger, critical, ASAP

### Medium Priority
slow, wifi issue, not working, broken, malfunction, problem, error, down

### Low Priority
cleaning, request, inquiry, question, suggestion, minor, routine

---

## 🔄 System Timings

- **Email Fetch:** Every 60 seconds (configurable)
- **Dashboard Refresh:** Every 30 seconds
- **Duplicate Window:** 24 hours

---

## 🎨 Status Options

- Pending
- In Progress
- Resolved
- Closed
- Rejected

---

## 📂 Important Files

### Backend
- `app.py` - Main server
- `email_fetcher.py` - Email handling
- `priority_classifier.py` - Classification
- `database.py` - Database ops
- `.env` - Configuration

### Frontend
- `src/App.js` - Main component
- `src/api.js` - API client
- `src/App.css` - Styles

---

## 🐛 Troubleshooting

### "Module not found"
```bash
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Database connection failed"
- Check MySQL is running
- Verify DB_PASSWORD in .env
- Run: `python init_db.py`

### "Email authentication failed"
- Use App Password, not regular password
- Enable 2-Step Verification
- Regenerate App Password

### "Port already in use"
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

## 📧 Test Email Template

### High Priority
```
To: your-email@gmail.com
Subject: URGENT: Fire in Building A
Body: There is a fire emergency on 3rd floor. 
      Immediate help needed ASAP!!!
```

### Medium Priority
```
To: your-email@gmail.com
Subject: WiFi not working
Body: Internet connection is very slow and keeps 
      disconnecting. Please fix this issue.
```

### Low Priority
```
To: your-email@gmail.com
Subject: Room cleaning request
Body: Could you schedule cleaning for my room 
      tomorrow? Thank you.
```

---

## 🔍 Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend opens in browser
- [ ] Database initialized
- [ ] Send test email
- [ ] Email appears in dashboard
- [ ] Priority correctly assigned
- [ ] Update status works
- [ ] Notification sends (if enabled)
- [ ] Search works
- [ ] Filters work

---

## 📖 Documentation

| Need | See |
|------|-----|
| Quick setup | QUICK_START.md |
| Detailed setup | SETUP_GUIDE.md |
| API info | API_DOCUMENTATION.md |
| How it works | PRIORITY_ALGORITHM.md |
| Testing | TESTING_GUIDE.md |
| Everything | DOCUMENTATION_INDEX.md |

---

## 💡 Pro Tips

1. **Background fetch runs automatically** - no need to click button
2. **Dashboard auto-refreshes** - leave it open for monitoring
3. **Search is instant** - no need to press Enter
4. **Filters are independent** - combine for precise results
5. **Check backend console** - see real-time processing logs
6. **Use sample data** - for initial testing (in init_db.py)
7. **Duplicate prevention** - same email won't process twice in 24h

---

## 🎯 Common Tasks

### Add Custom Keywords
Edit `backend/priority_classifier.py`:
```python
self.high_priority_keywords = [
    'fire', 'emergency',
    'your_custom_keyword'  # Add here
]
```

### Change Fetch Interval
Edit `backend/.env`:
```env
EMAIL_FETCH_INTERVAL=30  # seconds
```

### Export Data
Add to dashboard (future feature) or:
```bash
mysql -u root -p complaint_system
SELECT * FROM complaints INTO OUTFILE 'complaints.csv';
```

---

## ⚙️ Performance Tuning

### Database
- Indexes already optimized
- Consider archiving old complaints
- Regular OPTIMIZE TABLE

### Backend
- Adjust EMAIL_FETCH_INTERVAL
- Use connection pooling for scale
- Enable caching for stats

### Frontend
- Build for production: `npm run build`
- Deploy built files for better performance

---

## 🚀 Deployment Checklist

- [ ] Change SECRET_KEY in .env
- [ ] Use strong DB password
- [ ] Enable HTTPS
- [ ] Set up firewall rules
- [ ] Configure CORS for production domain
- [ ] Set FLASK_ENV=production
- [ ] Regular database backups
- [ ] Monitor error logs
- [ ] Set up uptime monitoring

---

## 📞 Support Resources

- **Setup Issues:** SETUP_GUIDE.md
- **API Questions:** API_DOCUMENTATION.md
- **Testing Help:** TESTING_GUIDE.md
- **Algorithm Details:** PRIORITY_ALGORITHM.md
- **Complete Guide:** DOCUMENTATION_INDEX.md

---

## 🎉 Success Indicators

✅ Backend console shows "Running on http://0.0.0.0:5000"
✅ Frontend opens without errors
✅ No red errors in browser console
✅ Test email appears in dashboard
✅ Status update works
✅ Stats display correctly

---

**Keep this card handy for quick reference!**

*Print this page or save as PDF for offline access*
