from typing import Any

def build_newsletter_html(articles: list[dict[str, str]], email: str) -> str:
    """
    Generates the HTML template for the newsletter.
    Presentation logic lives here, keeping EmailAgent clean.
    """

    html: str = """
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
</head>
<body style="font-family: 'Inter', -apple-system, sans-serif; color: #2D3436; line-height: 1.8; margin: 0; padding: 0; background-color: #0F172A;">
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #0F172A; padding: 40px 0;">
<tr>
<td align="center">

<div style="max-width: 650px; background: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.3);">

<div style="background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%); padding: 60px 40px; text-align: left;">
<h1 style="color:#ffffff;margin:0;font-family:'Playfair Display',serif;font-size:36px;line-height:1.2;letter-spacing:-0.5px;">
Your Daily <br><span style="color: #CCFF00;">Tech Digest</span>
</h1>

<div style="margin-top: 20px; height: 4px; width: 50px; background-color: #CCFF00; border-radius: 2px;"></div>

<p style="color: #E2E8F0; margin: 20px 0 0 0; font-size: 14px; letter-spacing: 1px; font-weight: 700; text-transform: uppercase;">
Curated By
<a href="https://github.com/erenYe0ger/agentic-ai-newsletter-service" style="color: #CCFF00; text-decoration: none; border-bottom:2px solid #CCFF00; padding-bottom:1px;">
Newsletter Agent
</a>
</p>
</div>

<div style="padding: 50px 40px;">
"""

    for a in articles:
        html += f"""
<div style="margin-bottom: 50px;">

<div style="display: inline-block; padding: 4px 12px; background: #F1F5F9; color: #6366F1; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;">
Latest Insight
</div>

<h2 style="font-family: 'Playfair Display', serif; font-size: 26px; color: #1E293B; margin: 0 0 15px 0; line-height: 1.2;">
{a['title']}
</h2>

<p style="font-size: 16px; color: #475569; margin-bottom: 25px; font-weight: 400;">
{a['summary']}
</p>

<a href="{a['link']}" style="color: #6366F1; text-decoration: none; font-weight: 700; font-size: 15px; border-bottom: 2px solid #6366F1; padding-bottom: 2px;">
Read the Full Report →
</a>

</div>

<div style="height: 1px; background: #F1F5F9; margin-bottom: 40px;"></div>
"""

    html += """
<div style="text-align: center; padding: 30px; background-color: #F8FAFC; border-radius: 16px; margin-top: 20px;">
<p style="font-size: 13px; color: #64748B; margin: 0;">
Generated for you by <strong>
<a href="https://github.com/erenYe0ger/agentic-ai-newsletter-service"
style="color:#2bce54; text-decoration:none; border-bottom:2px solid #2bce54; padding-bottom:1px;">
Newsletter Agent
</a></strong>.<br>
Keeping you updated with the latest in tech, every day.
</p>
</div>

</div>
</div>

<div style="color:#a2bad6;font-size:12px;margin-top:30px;text-align:center;">
<span>© 2026 Newsletter Agent. All rights reserved.</span><br>
<span>Made with ❤️ by Goutam</span><br>
<a href="https://agentic-ai-newsletter-service.onrender.com/unsubscribe?email={email}"
style="color:#ff6b6b;text-decoration:none;border-bottom:1px solid #ff6b6b;padding-bottom:1px;">
Unsubscribe
</a>
</div>

</td>
</tr>
</table>
</body>
</html>
"""

    return html