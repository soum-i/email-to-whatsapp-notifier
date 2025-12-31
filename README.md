# Email to WhatsApp Notification System

A Python-based automation tool that monitors incoming Gmail messages and sends real-time WhatsApp notifications using the Twilio API.

---

##  Features
- Detects new emails from Gmail inbox
- Sends WhatsApp alerts with email sender and subject
- Uses Google OAuth (no password storage)
- Prevents duplicate notifications
- Secure handling of credentials using environment variables

---

##  Tech Stack
- Python
- Gmail API
- Google OAuth 2.0
- Twilio WhatsApp API
- python-dotenv

---

## How It Works
1. Authenticates Gmail access using OAuth
2. Fetches the latest email from the inbox
3. Checks if the email was already processed
4. Sends a WhatsApp message for new emails
5. Stores the last email ID to avoid duplicates

---


