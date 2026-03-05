from app.services.email_service import EmailService
from app.utils.email_template import build_newsletter_html
import json
from typing import Any


class EmailAgent:
    """
    Agent responsible for sending the newsletter.
    Orchestrates template generation + email delivery.
    """

    def __init__(self) -> None:
        self.mailer: EmailService = EmailService()

        # Load recipients from config
        with open("app/config/recipients.json", "r") as f:
            data: dict[str, Any] = json.load(f)

        self.recipients: list[str] = data["recipients"]

    def send(self, articles: list[dict[str, str]]) -> None:
        """
        Generate HTML newsletter and send it to all recipients.
        """

        print("[EmailAgent] Sending Email...")

        # Build newsletter HTML from template utility
        html: str = build_newsletter_html(articles)

        for email in self.recipients:
            print(f"[EmailAgent] Sending to: {email}")

            self.mailer.send_email(
                to_email=email,
                subject="Your Daily Tech Digest",
                html_content=html
            )

        print("[EmailAgent] All emails delivered.")