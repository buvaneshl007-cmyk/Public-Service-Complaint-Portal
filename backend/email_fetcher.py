import imaplib
import email
from email.header import decode_header
import re
from config import Config
from priority_classifier import PriorityClassifier
from database import Database

class EmailFetcher:
    """Fetch and process emails from IMAP server"""
    
    def __init__(self):
        self.config = Config()
        self.classifier = PriorityClassifier()
        self.db = Database()
        self.mail = None
    
    def connect(self):
        """Connect to IMAP server"""
        try:
            self.mail = imaplib.IMAP4_SSL(self.config.IMAP_SERVER, self.config.IMAP_PORT)
            self.mail.login(self.config.EMAIL_ADDRESS, self.config.EMAIL_PASSWORD)
            print(f"✓ Connected to email server: {self.config.EMAIL_ADDRESS}")
            return True
        except Exception as e:
            print(f"✗ Email connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from IMAP server"""
        if self.mail:
            try:
                self.mail.logout()
            except:
                pass
    
    def fetch_unread_emails(self):
        """Fetch all unread emails from inbox"""
        try:
            # Select inbox
            self.mail.select('INBOX')
            
            # Search for unread emails
            status, messages = self.mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                print("No unread messages found")
                return []
            
            email_ids = messages[0].split()
            print(f"Found {len(email_ids)} unread email(s)")
            
            emails = []
            for email_id in email_ids:
                email_data = self._fetch_email(email_id)
                if email_data:
                    emails.append(email_data)
            
            return emails
        
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []
    
    def _fetch_email(self, email_id):
        """Fetch and parse individual email"""
        try:
            # Fetch email by ID
            status, msg_data = self.mail.fetch(email_id, '(RFC822)')
            
            if status != 'OK':
                return None
            
            # Parse email content
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extract sender
            sender = self._decode_email_header(msg.get('From'))
            sender_email = self._extract_email_address(sender)
            
            # Extract subject
            subject = self._decode_email_header(msg.get('Subject'))
            
            # Extract body
            body = self._get_email_body(msg)
            
            # Clean and extract meaningful content
            body_cleaned = self._clean_text(body)
            
            return {
                'sender_email': sender_email,
                'sender_name': sender,
                'subject': subject,
                'body': body_cleaned,
                'raw_body': body
            }
        
        except Exception as e:
            print(f"Error parsing email {email_id}: {e}")
            return None
    
    def _decode_email_header(self, header):
        """Decode email header"""
        if header is None:
            return ""
        
        decoded_parts = decode_header(header)
        decoded_string = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_string += part.decode(encoding or 'utf-8', errors='ignore')
            else:
                decoded_string += part
        
        return decoded_string
    
    def _extract_email_address(self, from_header):
        """Extract email address from From header"""
        email_pattern = r'<(.+?)>|([^\s]+@[^\s]+)'
        match = re.search(email_pattern, from_header)
        
        if match:
            return match.group(1) or match.group(2)
        return from_header
    
    def _get_email_body(self, msg):
        """Extract email body (plain text preferred)"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Skip attachments
                if "attachment" in content_disposition:
                    continue
                
                # Get text/plain content
                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        pass
                
                # Fallback to html
                elif content_type == "text/html" and not body:
                    try:
                        html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        body = self._html_to_text(html_content)
                    except:
                        pass
        else:
            # Not multipart
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                body = str(msg.get_payload())
        
        return body
    
    def _html_to_text(self, html):
        """Simple HTML to text conversion"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        # Decode HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        return text
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common email signatures
        text = re.split(r'\n\s*--\s*\n', text)[0]
        
        # Remove reply headers
        text = re.split(r'On .+?wrote:', text)[0]
        
        # Trim
        text = text.strip()
        
        return text[:5000]  # Limit length
    
    def process_and_store_emails(self):
        """Main function to fetch, classify, and store emails"""
        print("\n" + "="*60)
        print("Starting email fetch process...")
        print("="*60)
        
        # Connect to email
        if not self.connect():
            return {"success": False, "message": "Failed to connect to email server"}
        
        # Connect to database
        if not self.db.connect():
            self.disconnect()
            return {"success": False, "message": "Failed to connect to database"}
        
        try:
            # Fetch emails
            emails = self.fetch_unread_emails()
            
            if not emails:
                print("No new emails to process")
                return {"success": True, "message": "No new emails", "count": 0}
            
            processed_count = 0
            skipped_count = 0
            
            for email_data in emails:
                # Check for duplicates
                if self.db.check_duplicate_complaint(
                    email_data['sender_email'], 
                    email_data['subject'],
                    hours=24
                ):
                    print(f"⊗ Skipping duplicate: {email_data['subject'][:50]}")
                    skipped_count += 1
                    continue
                
                # Classify priority
                combined_text = f"{email_data['subject']} {email_data['body']}"
                priority = self.classifier.classify(combined_text)
                category = self.classifier.get_category(combined_text)
                
                # Store in database
                complaint_id = self.db.insert_complaint(
                    sender_email=email_data['sender_email'],
                    subject=email_data['subject'],
                    body=email_data['body'],
                    priority=priority,
                    category=category
                )
                
                if complaint_id:
                    processed_count += 1
                    print(f"✓ Complaint #{complaint_id} | Priority: {priority} | From: {email_data['sender_email']}")
                    print(f"  Subject: {email_data['subject'][:60]}")
                else:
                    print(f"✗ Failed to store complaint from {email_data['sender_email']}")
            
            print("-"*60)
            print(f"Processed: {processed_count} | Skipped: {skipped_count}")
            print("="*60 + "\n")
            
            return {
                "success": True,
                "message": f"Processed {processed_count} emails",
                "count": processed_count,
                "skipped": skipped_count
            }
        
        except Exception as e:
            print(f"Error in email processing: {e}")
            return {"success": False, "message": str(e)}
        
        finally:
            self.disconnect()
            self.db.close()

# Test function
if __name__ == "__main__":
    fetcher = EmailFetcher()
    result = fetcher.process_and_store_emails()
    print(result)
