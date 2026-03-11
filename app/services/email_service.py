import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import time

load_dotenv()


class EmailService:
    """
    Handles sending emails via Gmail SMTP.
    """

    def send_email(self, to_email: str, subject: str, html_content: str) -> None:

        msg: MIMEText = MIMEText(html_content, "html")
        msg["Subject"] = subject
        msg["From"] = os.getenv("EMAIL_ADDRESS")
        msg["To"] = to_email

        retries = 3

        for attempt in range(retries):

            try:
                # Connect to Gmail SMTP with timeout
                with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
                    smtp.starttls()

                    smtp.login(
                        os.getenv("EMAIL_ADDRESS"),
                        os.getenv("EMAIL_APP_PASSWORD")
                    )

                    smtp.send_message(msg)

                print(f"[EmailService] Email sent to {to_email}")
                return

            except Exception as e:

                print(f"[EmailService] Attempt {attempt+1} failed: {e}")

                if attempt < retries - 1:
                    time.sleep(5)
                else:
                    print("[EmailService] Email delivery failed.")