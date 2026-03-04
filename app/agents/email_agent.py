from app.services.email_service import EmailService
from app.utils.email_template import build_newsletter_html
import json


class EmailAgent:
    """
    Agent responsible for sending the newsletter.
    Orchestrates template generation + email delivery.
    """

    def __init__(self):
        self.mailer = EmailService()

        # Load recipients from config
        with open("app/config/recipients.json", "r") as f:
            data = json.load(f)

        self.recipients = data["recipients"]

    def send(self, articles: list[dict]) -> None:
        """
        Generate HTML newsletter and send it to all recipients.
        """

        print("[EmailAgent] Sending Email...")

        # Build newsletter HTML from template utility
        html = build_newsletter_html(articles)

        for email in self.recipients:
            print(f"[EmailAgent] Sending to: {email}")

            self.mailer.send_email(
                to_email=email,
                subject="Your Daily Tech Digest",
                html_content=html
            )

        print("[EmailAgent] All emails delivered.")