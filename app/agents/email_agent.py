from app.services.email_service import EmailService
import json
import os

class EmailAgent:
    def __init__(self):
        self.mailer = EmailService()

        # Load recipients list
        config_path = os.path.join("app", "config", "recipients.json")
        with open(config_path, "r") as f:
            data = json.load(f)

        self.recipients = data.get("recipients", [])

    def send(self, articles):
        print("[EmailAgent] Sending Email...")

        html = "<h2>Your Daily Tech Digest</h2>"
        for a in articles:
            html += f"<h3>{a['title']}</h3>"
            html += f"<p>{a['summary']}</p>"
            html += f"<a href='{a['link']}'>Read more</a><br><br>"

        # Send to every recipient
        for email in self.recipients:
            print(f"[EmailAgent] Sending to: {email}")
            self.mailer.send_email(
                to_email=email,
                subject="Your Daily Tech Digest",
                html_content=html
            )

        print("[EmailAgent] All emails delivered.")