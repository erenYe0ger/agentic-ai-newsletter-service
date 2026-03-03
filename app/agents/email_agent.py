from app.services.email_service import EmailService

class EmailAgent:
    def __init__(self):
        self.mailer = EmailService()

    def send(self, to_email, articles):
        print("[EmailAgent] Sending Email...")

        html = "<h2>Your Daily Tech Digest</h2>"
        for a in articles:
            html += f"<h3>{a['title']}</h3>"
            html += f"<p>{a['summary']}</p>"
            html += f"<a href='{a['link']}'>Read more</a><br><br>"

        self.mailer.send_email(
            to_email=to_email,
            subject="Your Daily Tech Digest",
            html_content=html
        )