from app.services.email_service import EmailService
from app.utils.newsletter_template import build_newsletter_html
from app.db.session import engine
from sqlalchemy import text


class EmailAgent:
    """
    Agent responsible for sending the newsletter.
    Orchestrates template generation + email delivery.
    """

    def __init__(self) -> None:
        self.mailer: EmailService = EmailService()

    def send(self, articles: list[dict[str, str]]) -> None:

        print("[EmailAgent] Sending Email...")

        with engine.connect() as conn:
            result = conn.execute(text("SELECT email FROM subscribers"))
            emails: list[str] = [row[0] for row in result]

        for email in emails:

            print(f"[EmailAgent] Sending to: {email}")

            html: str = build_newsletter_html(articles, email)

            self.mailer.send_email(
                to_email=email,
                subject="Your Daily Tech Digest",
                html_content=html
            )

        print("[EmailAgent] All emails delivered.")


    def send_to_user(self, articles: list[dict[str, str]], email: str) -> None:

        print(f"[EmailAgent] Sending digest to new subscriber: {email}")

        html: str = build_newsletter_html(articles, email)

        self.mailer.send_email(
            to_email=email,
            subject="Your Daily Tech Digest",
            html_content=html
        )