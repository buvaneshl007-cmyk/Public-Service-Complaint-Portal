# 📊 System Flow Diagrams

Visual representations of how the Complaint Priority Management System works.

---

## 🔄 Complete System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER SENDS EMAIL COMPLAINT                    │
│                  To: complaints@gmail.com                        │
│                  Subject: "Fire in Building A"                   │
│                  Body: "Emergency situation..."                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
         ┌───────────────────────────────────────┐
         │   GMAIL INBOX (IMAP)                  │
         │   - Email stored in inbox             │
         │   - Marked as UNREAD                  │
         └───────────────┬───────────────────────┘
                         │
                         │ ◄── Backend checks every 60 seconds
                         │
                         ▼
         ┌───────────────────────────────────────┐
         │   EMAIL FETCHER MODULE                │
         │   1. Connect via IMAP                 │
         │   2. Search for UNSEEN emails         │
         │   3. Parse email components:          │
         │      - Sender email                   │
         │      - Subject line                   │
         │      - Body text                      │
         │   4. Clean and normalize text         │
         └───────────────┬───────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────────────┐
         │   DUPLICATE CHECK                     │
         │   - Same sender?                      │
         │   - Same subject?                     │
         │   - Within 24 hours?                  │
         │                                       │
         │   YES → Skip (avoid duplicates)       │
         │   NO  → Continue processing           │
         └───────────────┬───────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────────────┐
         │   PRIORITY CLASSIFIER ENGINE          │
         │                                       │
         │   Input: Subject + Body               │
         │                                       │
         │   Step 1: Keyword Matching            │
         │   ┌─────────────────────────────┐    │
         │   │ High Keywords: fire,        │    │
         │   │ emergency, urgent, leak...  │    │
         │   │ Match count: 2              │    │
         │   └─────────────────────────────┘    │
         │                                       │
         │   Step 2: Urgency Pattern Check       │
         │   ┌─────────────────────────────┐    │
         │   │ Patterns: ASAP, !!!,        │    │
         │   │ immediately                 │    │
         │   │ Match: YES (+2 boost)       │    │
         │   └─────────────────────────────┘    │
         │                                       │
         │   Step 3: Decision                    │
         │   ┌─────────────────────────────┐    │
         │   │ High score > 0 → HIGH       │    │
         │   │ Medium > Low → MEDIUM       │    │
         │   │ Else → LOW                  │    │
         │   └─────────────────────────────┘    │
         │                                       │
         │   Output: Priority = HIGH             │
         └───────────────┬───────────────────────┘
                         │
                         ├────────────────────┐
                         │                    │
                         ▼                    ▼
         ┌───────────────────────┐  ┌───────────────────────┐
         │ CATEGORY CLASSIFIER   │  │ Priority: HIGH        │
         │                       │  │ Category: Safety      │
         │ Keywords matched:     │  │ Status: Pending       │
         │ - fire, building      │  │                       │
         │                       │  │                       │
         │ Category: Safety      │  │                       │
         └───────────┬───────────┘  └───────────┬───────────┘
                     │                          │
                     └──────────┬───────────────┘
                                │
                                ▼
                ┌───────────────────────────────────────┐
                │   MySQL DATABASE                      │
                │                                       │
                │   INSERT INTO complaints:             │
                │   ┌─────────────────────────────────┐│
                │   │ id: 42                          ││
                │   │ sender_email: user@example.com  ││
                │   │ subject: "Fire in Building A"   ││
                │   │ body: "Emergency situation..."  ││
                │   │ priority: "High"                ││
                │   │ category: "Safety"              ││
                │   │ status: "Pending"               ││
                │   │ created_at: 2026-01-08 10:30   ││
                │   └─────────────────────────────────┘│
                │                                       │
                │   ✓ Stored successfully               │
                └───────────────┬───────────────────────┘
                                │
                                ▼
                ┌───────────────────────────────────────┐
                │   BACKEND LOGS                        │
                │                                       │
                │   ✓ Complaint #42 | Priority: High   │
                │     From: user@example.com            │
                │     Subject: Fire in Building A       │
                └───────────────────────────────────────┘
                                │
                                │
                                ▼
        ┌───────────────────────────────────────────────┐
        │   REACT DASHBOARD (Auto-refresh every 30s)     │
        │                                                │
        │   API Call: GET /api/complaints                │
        │             GET /api/stats                     │
        │                                                │
        │   ┌─────────────────────────────────────┐     │
        │   │  📊 STATISTICS CARDS                │     │
        │   │  Total: 42  High: 5  Medium: 20     │     │
        │   └─────────────────────────────────────┘     │
        │                                                │
        │   ┌─────────────────────────────────────┐     │
        │   │  🔍 SEARCH & FILTERS                │     │
        │   │  [Search...] [Priority ▼] [Status ▼]│     │
        │   └─────────────────────────────────────┘     │
        │                                                │
        │   ┌─────────────────────────────────────┐     │
        │   │  📋 COMPLAINTS TABLE                │     │
        │   │  ┌──┬──────┬────────┬──────────┐   │     │
        │   │  │42│[HIGH]│user@...│Fire in...│   │     │
        │   │  │41│[MED] │test@...│WiFi slow │   │     │
        │   │  └──┴──────┴────────┴──────────┘   │     │
        │   └─────────────────────────────────────┘     │
        │                                                │
        │   Admin clicks [View] button                  │
        └────────────────────┬──────────────────────────┘
                             │
                             ▼
        ┌───────────────────────────────────────────────┐
        │   COMPLAINT DETAIL MODAL                       │
        │                                                │
        │   Complaint #42                                │
        │   Priority: [HIGH]                             │
        │   Status: [Pending]                            │
        │   Sender: user@example.com                     │
        │   Subject: Fire in Building A                  │
        │   Category: Safety                             │
        │   Body: Emergency situation...                 │
        │                                                │
        │   Update Status: [In Progress ▼]              │
        │   ☑ Send email notification                   │
        │                                                │
        │   [Cancel]  [Update Status]                    │
        └────────────────────┬──────────────────────────┘
                             │
                             │ Admin clicks Update
                             │
                             ▼
        ┌───────────────────────────────────────────────┐
        │   API: PUT /api/complaints/42                  │
        │   Body: {                                      │
        │     "status": "In Progress",                   │
        │     "send_notification": true                  │
        │   }                                            │
        └────────────────────┬──────────────────────────┘
                             │
                             ├──────────────┬─────────────┐
                             │              │             │
                             ▼              ▼             ▼
        ┌────────────────┐ ┌────────────┐ ┌──────────────────┐
        │ Update DB      │ │ Log Action │ │ Send Email       │
        │ Status changed │ │ to admin_  │ │ Notification     │
        │ to "In Progress"│ │ actions    │ │                  │
        └────────────────┘ └────────────┘ └────────┬─────────┘
                                                    │
                                                    ▼
                                   ┌────────────────────────────┐
                                   │  EMAIL NOTIFIER (SMTP)     │
                                   │                            │
                                   │  To: user@example.com      │
                                   │  Subject: Complaint Status │
                                   │          Updated - #42     │
                                   │                            │
                                   │  Body: Your complaint is   │
                                   │  now In Progress...        │
                                   └────────────┬───────────────┘
                                                │
                                                ▼
                                   ┌────────────────────────────┐
                                   │  USER RECEIVES EMAIL       │
                                   │  ✓ Notification delivered  │
                                   └────────────────────────────┘
```

---

## 🔀 Priority Classification Logic

```
                    ┌─────────────────────┐
                    │   EMAIL TEXT        │
                    │  (Subject + Body)   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Convert to         │
                    │  Lowercase          │
                    └──────────┬──────────┘
                               │
                   ┌───────────┴───────────┐
                   │                       │
                   ▼                       ▼
        ┌──────────────────┐    ┌──────────────────┐
        │ Count High       │    │ Check Urgency    │
        │ Keywords         │    │ Patterns         │
        │                  │    │                  │
        │ fire, emergency, │    │ ASAP, !!!,       │
        │ urgent, leak...  │    │ immediately      │
        │                  │    │                  │
        │ Count: 2         │    │ Found: YES       │
        └─────────┬────────┘    └────────┬─────────┘
                  │                      │
                  │   ┌──────────────────┘
                  │   │
                  ▼   ▼
        ┌──────────────────────┐
        │  High Score = 2 + 2  │
        │  (keywords + urgency)│
        │  Score: 4            │
        └──────────┬───────────┘
                   │
        ┌──────────────────────┐
        │ Count Medium         │
        │ Keywords             │
        │                      │
        │ slow, not working... │
        │ Count: 0             │
        └──────────┬───────────┘
                   │
        ┌──────────────────────┐
        │ Count Low            │
        │ Keywords             │
        │                      │
        │ request, cleaning... │
        │ Count: 0             │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  DECISION LOGIC      │
        │                      │
        │  if high_score > 0:  │
        │    return "High" ✓   │
        │  elif medium > low:  │
        │    return "Medium"   │
        │  elif medium > 0:    │
        │    return "Medium"   │
        │  else:               │
        │    return "Low"      │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   RESULT: HIGH       │
        └──────────────────────┘
```

---

## 🗄️ Database Operations Flow

```
┌─────────────────────────────────────────────────────────┐
│                    NEW COMPLAINT                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
    ┌────────────────────────────────────┐
    │  database.insert_complaint()       │
    │                                    │
    │  INSERT INTO complaints            │
    │  (sender_email, subject, body,     │
    │   priority, category, status,      │
    │   created_at)                      │
    │  VALUES (?, ?, ?, ?, ?, ?, ?)      │
    └────────────┬───────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────┐
    │   MySQL Database                   │
    │                                    │
    │   complaints table                 │
    │   ┌──────────────────────────┐    │
    │   │ New row inserted         │    │
    │   │ id: 42 (AUTO_INCREMENT)  │    │
    │   └──────────────────────────┘    │
    │                                    │
    │   Indexes updated:                 │
    │   - idx_priority                   │
    │   - idx_status                     │
    │   - idx_sender_email               │
    │   - idx_created_at                 │
    └────────────┬───────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────┐
    │  Return complaint_id: 42           │
    └────────────────────────────────────┘


┌─────────────────────────────────────────────────────────┐
│               STATUS UPDATE REQUEST                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
    ┌────────────────────────────────────┐
    │  database.update_complaint_status()│
    │                                    │
    │  UPDATE complaints                 │
    │  SET status = ?,                   │
    │      updated_at = NOW()            │
    │  WHERE id = ?                      │
    └────────────┬───────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────┐
    │   MySQL Database                   │
    │                                    │
    │   Row updated                      │
    │   Timestamp automatically set      │
    └────────────┬───────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────┐
    │  Log to admin_actions table        │
    │                                    │
    │  INSERT INTO admin_actions         │
    │  (complaint_id, action_type,       │
    │   old_value, new_value)            │
    └────────────────────────────────────┘
```

---

## 🔄 Background Scheduler Flow

```
┌──────────────────────────────────────┐
│   Flask App Starts                   │
└────────────────┬─────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│   APScheduler Initialized            │
│                                      │
│   scheduler = BackgroundScheduler()  │
│   scheduler.add_job(                 │
│     func=fetch_emails_job,           │
│     trigger="interval",              │
│     seconds=60                       │
│   )                                  │
│   scheduler.start()                  │
└────────────────┬─────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│   ⏰ Every 60 Seconds                │
└────────────────┬─────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│   fetch_emails_job() executes        │
│                                      │
│   1. Connect to Gmail (IMAP)         │
│   2. Search for unread emails        │
│   3. Parse each email                │
│   4. Classify priority               │
│   5. Store in database               │
│   6. Mark email as read (optional)   │
└────────────────┬─────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│   Log results to console             │
│   "Processed 3 emails"               │
└────────────────┬─────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│   Wait for next interval (60s)       │
└──────────────────────────────────────┘
                 │
                 └──────┐
                        │
                 ┌──────┘
                 │
                 ▼
          (Repeat forever)
```

---

## 🌐 API Request-Response Flow

```
FRONTEND                    BACKEND                    DATABASE

  │                           │                          │
  │  GET /api/complaints      │                          │
  ├──────────────────────────>│                          │
  │                           │                          │
  │                           │  SELECT * FROM           │
  │                           │  complaints              │
  │                           ├─────────────────────────>│
  │                           │                          │
  │                           │  <── Rows returned       │
  │                           │<─────────────────────────┤
  │                           │                          │
  │  <── JSON response        │                          │
  │<──────────────────────────┤                          │
  │  {complaints: [...]}      │                          │
  │                           │                          │
  │                           │                          │
  │  PUT /api/complaints/42   │                          │
  │  {status: "Resolved"}     │                          │
  ├──────────────────────────>│                          │
  │                           │                          │
  │                           │  UPDATE complaints       │
  │                           │  SET status = 'Resolved' │
  │                           ├─────────────────────────>│
  │                           │                          │
  │                           │  <── Success             │
  │                           │<─────────────────────────┤
  │                           │                          │
  │                           │  Send Email (optional)   │
  │                           ├──> SMTP Server           │
  │                           │                          │
  │  <── {success: true}      │                          │
  │<──────────────────────────┤                          │
  │                           │                          │
```

---

## 📧 Email Notification Flow

```
┌─────────────────────────────────┐
│  Admin Updates Status           │
│  to "Resolved"                  │
│  ☑ Send notification checked    │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  email_notifier.                │
│  send_complaint_resolved()      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Build Email Message            │
│                                 │
│  From: complaints@gmail.com     │
│  To: user@example.com           │
│  Subject: Complaint Resolved #42│
│                                 │
│  Create HTML template           │
│  Create plain text version      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Connect to SMTP Server         │
│  (smtp.gmail.com:587)           │
│                                 │
│  1. STARTTLS (encryption)       │
│  2. LOGIN with app password     │
│  3. SEND email                  │
│  4. QUIT                        │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Email Delivered ✓              │
│                                 │
│  User receives notification     │
│  in their inbox                 │
└─────────────────────────────────┘
```

---

These diagrams illustrate the complete data flow and system interactions!
