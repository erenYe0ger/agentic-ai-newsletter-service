import os
import base64
import pickle
from email.mime.text import MIMEText
from googleapiclient.discovery import build


class EmailService:
    """
    Sends emails using Gmail API.
    Works on cloud platforms (no SMTP).
    """

    def __init__(self):

        # Decode Gmail token from environment variable
        token_bytes = base64.b64decode(os.getenv("GMAIL_TOKEN"))

        # Load credentials
        creds = pickle.loads(token_bytes)

        # Gmail API service
        self.service = build("gmail", "v1", credentials=creds)

        self.sender = os.getenv("EMAIL_ADDRESS")

    def send_email(self, to_email: str, subject: str, html_content: str):

        # Build email message
        message = MIMEText(html_content, "html")
        message["to"] = to_email
        message["from"] = self.sender
        message["subject"] = subject

        # Encode for Gmail API
        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        # Send email
        self.service.users().messages().send(
            userId="me",
            body={"raw": raw_message}
        ).execute()

        print(f"[EmailService] Sent to {to_email}")