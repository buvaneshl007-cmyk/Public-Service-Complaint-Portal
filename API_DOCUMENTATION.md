# 📋 API Documentation

## Base URL
```
http://localhost:5000/api
```

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running and scheduler is active.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-08T10:30:00.000Z",
  "scheduler_running": true
}
```

---

### 2. Get All Complaints

**GET** `/complaints`

Retrieve all complaints with optional filtering.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `priority` | string | Filter by priority: `High`, `Medium`, `Low` |
| `status` | string | Filter by status: `Pending`, `In Progress`, `Resolved`, `Closed`, `Rejected` |
| `search` | string | Search in email, subject, or body |
| `limit` | number | Number of results (default: 100) |
| `offset` | number | Pagination offset (default: 0) |

**Example Request:**
```bash
GET /api/complaints?priority=High&status=Pending&limit=20
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "complaints": [
    {
      "id": 1,
      "sender_email": "user@example.com",
      "subject": "No power in Block B",
      "body": "There is no electricity...",
      "priority": "High",
      "category": "Electrical",
      "status": "Pending",
      "created_at": "2026-01-08T09:15:00",
      "updated_at": "2026-01-08T09:15:00"
    }
  ]
}
```

---

### 3. Get Single Complaint

**GET** `/complaints/<id>`

Retrieve a specific complaint by ID.

**Example Request:**
```bash
GET /api/complaints/1
```

**Response:**
```json
{
  "success": true,
  "complaint": {
    "id": 1,
    "sender_email": "user@example.com",
    "subject": "No power in Block B",
    "body": "Full complaint text...",
    "priority": "High",
    "category": "Electrical",
    "status": "Pending",
    "created_at": "2026-01-08T09:15:00",
    "updated_at": "2026-01-08T09:15:00"
  }
}
```

**Error Response (404):**
```json
{
  "error": "Complaint not found"
}
```

---

### 4. Update Complaint Status

**PUT** `/complaints/<id>`

Update the status of a complaint.

**Request Body:**
```json
{
  "status": "In Progress",
  "send_notification": true
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | New status: `Pending`, `In Progress`, `Resolved`, `Closed`, `Rejected` |
| `send_notification` | boolean | No | Send email to customer (default: false) |

**Example Request:**
```bash
PUT /api/complaints/1
Content-Type: application/json

{
  "status": "Resolved",
  "send_notification": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Status updated successfully",
  "old_status": "In Progress",
  "new_status": "Resolved"
}
```

**Error Response (400):**
```json
{
  "error": "Invalid status. Must be one of: Pending, In Progress, Resolved, Closed, Rejected"
}
```

---

### 5. Get Statistics

**GET** `/stats`

Get dashboard statistics including total counts and breakdowns.

**Response:**
```json
{
  "success": true,
  "stats": {
    "total": 25,
    "by_priority": {
      "High": 5,
      "Medium": 12,
      "Low": 8
    },
    "by_status": {
      "Pending": 10,
      "In Progress": 8,
      "Resolved": 7
    }
  }
}
```

---

### 6. Manually Fetch Emails

**POST** `/fetch-emails`

Manually trigger email fetching process.

**Response:**
```json
{
  "success": true,
  "message": "Processed 3 emails",
  "count": 3,
  "skipped": 0
}
```

---

### 7. Test Email Notification

**POST** `/test-notification`

Send a test email notification.

**Request Body:**
```json
{
  "email": "test@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Test email sent"
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Data Models

### Complaint Object

```typescript
{
  id: number,
  sender_email: string,
  subject: string,
  body: string,
  priority: "High" | "Medium" | "Low",
  category: string,
  status: "Pending" | "In Progress" | "Resolved" | "Closed" | "Rejected",
  created_at: string (ISO 8601),
  updated_at: string (ISO 8601)
}
```

---

## Example Usage

### Python
```python
import requests

# Get all high priority complaints
response = requests.get(
    'http://localhost:5000/api/complaints',
    params={'priority': 'High'}
)
complaints = response.json()['complaints']

# Update complaint status
requests.put(
    'http://localhost:5000/api/complaints/1',
    json={
        'status': 'Resolved',
        'send_notification': True
    }
)
```

### JavaScript/Axios
```javascript
import axios from 'axios';

// Get all complaints
const { data } = await axios.get('/api/complaints');

// Update complaint
await axios.put(`/api/complaints/${id}`, {
  status: 'In Progress',
  send_notification: true
});

// Get statistics
const stats = await axios.get('/api/stats');
```

### cURL
```bash
# Get complaints
curl http://localhost:5000/api/complaints

# Update status
curl -X PUT http://localhost:5000/api/complaints/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"Resolved","send_notification":true}'

# Fetch emails
curl -X POST http://localhost:5000/api/fetch-emails
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider adding rate limiting middleware.

---

## CORS

CORS is enabled for origins specified in the `CORS_ORIGINS` environment variable (default: `http://localhost:3000`).
