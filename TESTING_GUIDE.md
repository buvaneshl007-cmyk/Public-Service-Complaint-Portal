# 🧪 Testing Guide

## Overview

This guide helps you test all features of the Complaint Priority Management System.

---

## ✅ Pre-Testing Checklist

- [ ] Backend server running on port 5000
- [ ] Frontend server running on port 3000
- [ ] MySQL database initialized
- [ ] Gmail credentials configured
- [ ] .env file properly set up

---

## 🎯 Test Scenarios

### Test 1: High Priority Email

**Objective:** Verify high priority classification

**Steps:**
1. Send email to your configured Gmail address
2. **Subject:** `URGENT: Fire in Building A`
3. **Body:**
   ```
   There is a fire on the 3rd floor of Building A.
   The situation is critical and requires immediate attention.
   Smoke is spreading rapidly. Please send help ASAP!
   ```
4. Wait 60 seconds or click "Fetch Emails" in dashboard
5. Check dashboard

**Expected Result:**
- ✅ Complaint appears in dashboard
- ✅ Priority: **HIGH** (Red badge)
- ✅ Category: **Safety**
- ✅ Status: **Pending**

---

### Test 2: Medium Priority Email

**Objective:** Verify medium priority classification

**Steps:**
1. Send email
2. **Subject:** `WiFi Connection Issues`
3. **Body:**
   ```
   The internet connection in Room 301 is very slow.
   WiFi keeps disconnecting frequently.
   This is affecting my work. Please fix this issue.
   ```
4. Fetch emails

**Expected Result:**
- ✅ Priority: **MEDIUM** (Orange badge)
- ✅ Category: **Network/IT**

---

### Test 3: Low Priority Email

**Objective:** Verify low priority classification

**Steps:**
1. Send email
2. **Subject:** `Room Cleaning Request`
3. **Body:**
   ```
   Hello,
   Could you please schedule a cleaning service for my room?
   Tomorrow afternoon would be convenient.
   Thank you!
   ```
4. Fetch emails

**Expected Result:**
- ✅ Priority: **LOW** (Green badge)
- ✅ Category: **Cleaning**

---

### Test 4: Search Functionality

**Objective:** Test search feature

**Steps:**
1. Ensure you have multiple complaints in database
2. In search box, type: `fire`
3. Press Enter or wait for auto-search

**Expected Result:**
- ✅ Only complaints with "fire" in email/subject/body appear
- ✅ Other complaints filtered out

---

### Test 5: Filter by Priority

**Objective:** Test priority filter

**Steps:**
1. Select "High" from Priority dropdown
2. Observe table

**Expected Result:**
- ✅ Only high priority complaints shown
- ✅ Count updates accordingly

**Repeat for:**
- Medium priority
- Low priority
- All priorities (default)

---

### Test 6: Filter by Status

**Objective:** Test status filter

**Steps:**
1. Select "Pending" from Status dropdown

**Expected Result:**
- ✅ Only pending complaints shown

**Repeat for:**
- In Progress
- Resolved
- All statuses (default)

---

### Test 7: View Complaint Details

**Objective:** Test detail modal

**Steps:**
1. Click "View" button on any complaint
2. Modal should open

**Expected Result:**
- ✅ Modal displays with all details
- ✅ Priority badge shown
- ✅ Status badge shown
- ✅ Full email body visible
- ✅ Sender email displayed
- ✅ Category shown
- ✅ Timestamps formatted correctly

---

### Test 8: Update Complaint Status

**Objective:** Test status update feature

**Steps:**
1. Open complaint detail modal
2. Change status from "Pending" to "In Progress"
3. Uncheck "Send email notification"
4. Click "Update Status"

**Expected Result:**
- ✅ Success message appears
- ✅ Modal closes
- ✅ Table updates with new status
- ✅ Status badge color changes
- ✅ No email sent (because notification unchecked)

---

### Test 9: Email Notification

**Objective:** Test email notification feature

**Steps:**
1. Use your own email as sender for a test complaint
2. Update status to "Resolved"
3. **Check** "Send email notification"
4. Click "Update Status"
5. Check your inbox

**Expected Result:**
- ✅ Email received in inbox
- ✅ Subject: "Complaint Resolved - #[ID]"
- ✅ HTML formatted email
- ✅ Contains complaint details

---

### Test 10: Manual Email Fetch

**Objective:** Test manual fetch button

**Steps:**
1. Send a new test email
2. Click "📧 Fetch Emails" button in dashboard
3. Wait for response

**Expected Result:**
- ✅ Button shows "Fetching..." while processing
- ✅ Alert shows success message
- ✅ New complaint appears immediately
- ✅ Last fetch timestamp updates

---

### Test 11: Auto-Refresh

**Objective:** Verify dashboard auto-refreshes

**Steps:**
1. Keep dashboard open
2. Send a new email complaint
3. Wait 60 seconds (don't click fetch button)
4. Observe dashboard

**Expected Result:**
- ✅ New complaint appears automatically
- ✅ Stats update automatically
- ✅ No page reload required

---

### Test 12: Statistics Cards

**Objective:** Verify stats accuracy

**Steps:**
1. Count high priority complaints manually
2. Check "High Priority" stat card
3. Repeat for other categories

**Expected Result:**
- ✅ Total count matches database
- ✅ Priority breakdown accurate
- ✅ Status breakdown accurate

---

### Test 13: Multiple Categories

**Objective:** Test category classification

Send emails with different categories:

**Electrical:**
```
Subject: Power Outage
Body: No electricity in the building. Circuit breaker tripped.
```
Expected: Category = **Electrical**

**Plumbing:**
```
Subject: Water Leak
Body: Pipe is leaking in the bathroom. Water everywhere.
```
Expected: Category = **Plumbing**

**HVAC:**
```
Subject: AC Problem
Body: Air conditioning not cooling. Very hot in the room.
```
Expected: Category = **HVAC**

---

### Test 14: Duplicate Detection

**Objective:** Test duplicate prevention

**Steps:**
1. Send email with subject "Test Duplicate"
2. Wait for it to be processed
3. Send another email with same subject from same sender
4. Fetch emails

**Expected Result:**
- ✅ First email processed
- ✅ Second email skipped (duplicate)
- ✅ Backend console shows "Skipping duplicate" message

---

### Test 15: Clear Filters

**Objective:** Test clear filters button

**Steps:**
1. Apply search: "fire"
2. Apply priority filter: "High"
3. Apply status filter: "Pending"
4. Click "Clear Filters"

**Expected Result:**
- ✅ Search box cleared
- ✅ Priority dropdown reset to "All"
- ✅ Status dropdown reset to "All"
- ✅ All complaints shown

---

## 🔧 API Testing

### Using Browser (Simple)

**Health Check:**
```
http://localhost:5000/api/health
```

**Get All Complaints:**
```
http://localhost:5000/api/complaints
```

**Get Statistics:**
```
http://localhost:5000/api/stats
```

### Using cURL (Advanced)

**Get Complaints:**
```bash
curl http://localhost:5000/api/complaints
```

**Update Status:**
```bash
curl -X PUT http://localhost:5000/api/complaints/1 \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"Resolved\",\"send_notification\":true}"
```

**Fetch Emails:**
```bash
curl -X POST http://localhost:5000/api/fetch-emails
```

---

## 🐛 Error Testing

### Test Database Connection Error

**Steps:**
1. Stop MySQL service
2. Try to load dashboard

**Expected:**
- ✅ Error message in backend console
- ✅ API returns 500 error
- ✅ Frontend shows error state

### Test Invalid Email Credentials

**Steps:**
1. Set wrong EMAIL_PASSWORD in .env
2. Restart backend
3. Try to fetch emails

**Expected:**
- ✅ Error in console: "Authentication failed"
- ✅ Fetch returns error message

### Test Invalid Status Update

**Steps:**
1. Try to update status via API with invalid value

```bash
curl -X PUT http://localhost:5000/api/complaints/1 \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"InvalidStatus\"}"
```

**Expected:**
- ✅ 400 error response
- ✅ Error message: "Invalid status"

---

## 📊 Performance Testing

### Load Test Email Parsing

**Steps:**
1. Send 50 emails at once
2. Click "Fetch Emails"
3. Monitor backend console

**Expected:**
- ✅ All emails processed
- ✅ Processing time < 30 seconds
- ✅ No crashes

### Dashboard Responsiveness

**Steps:**
1. Load 1000+ complaints in database
2. Open dashboard
3. Try filters and search

**Expected:**
- ✅ Page loads < 2 seconds
- ✅ Filters respond instantly
- ✅ Search works smoothly

---

## ✅ Acceptance Criteria

### Backend

- [ ] Email fetching works without errors
- [ ] Priority classification is accurate (>85%)
- [ ] Database stores all complaints
- [ ] API responds within 500ms
- [ ] Background scheduler runs continuously
- [ ] Error handling prevents crashes
- [ ] Notifications send successfully

### Frontend

- [ ] Dashboard loads without errors
- [ ] All stats display correctly
- [ ] Search returns relevant results
- [ ] Filters work independently
- [ ] Modal opens and closes properly
- [ ] Status updates reflect immediately
- [ ] UI is responsive and professional

### Integration

- [ ] End-to-end flow works (email → dashboard)
- [ ] Real-time updates function
- [ ] Notifications reach inbox
- [ ] No CORS errors
- [ ] No console errors

---

## 📝 Test Checklist Summary

Copy this for quick testing:

```
☐ High priority email classification
☐ Medium priority email classification
☐ Low priority email classification
☐ Search functionality
☐ Priority filter
☐ Status filter
☐ View complaint details
☐ Update status (no notification)
☐ Update status (with notification)
☐ Manual email fetch
☐ Auto-refresh verification
☐ Statistics accuracy
☐ Category classification
☐ Duplicate detection
☐ Clear filters
☐ API health check
☐ Error handling
☐ Performance under load
```

---

## 🎉 Testing Complete!

If all tests pass:
- ✅ System is fully functional
- ✅ Ready for production deployment
- ✅ All features working as designed

---

## 📞 Troubleshooting Test Failures

### Emails not appearing
- Check backend console for errors
- Verify EMAIL_ADDRESS and EMAIL_PASSWORD
- Ensure Gmail allows IMAP access
- Check spam folder

### Wrong priority assigned
- Review keyword lists in `priority_classifier.py`
- Check email content for expected keywords
- Enable debug logging

### Stats not updating
- Check database connection
- Verify queries in `database.py`
- Check browser console for API errors

### Notifications not sending
- Verify SMTP settings
- Check EMAIL_PASSWORD (App Password)
- Test with `/api/test-notification`

---

**Happy Testing! 🚀**
