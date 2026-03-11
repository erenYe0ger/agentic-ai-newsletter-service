def wrap_email(content: str) -> str:
    """
    Wrap custom content inside the newsletter layout.
    Used for subscribe/unsubscribe emails.
    """

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agentic AI | Notification</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
</head>

<body style="font-family: 'Inter', -apple-system, sans-serif; color: #2D3436; line-height: 1.8; margin: 0; padding: 0; background-color: #0F172A;">

<table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #0F172A; padding: 40px 0;">
<tr>
<td align="center">

<div style="max-width: 650px; background: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.3); text-align: left;">

<div style="background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%); padding: 60px 40px; text-align: left;">
<h1 style="color:#ffffff; margin:0; font-family:'Playfair Display',serif; font-size:36px; line-height:1.2; letter-spacing:-0.5px;">
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

<div style="padding: 60px 40px; text-align: center;">

{content}

</div>

<div style="padding: 0 40px 40px 40px;">
<div style="text-align: center; padding: 30px; background-color: #F8FAFC; border-radius: 16px;">
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

<div style="color:#a2bad6; font-size:12px; margin-top:30px; text-align:center;">
<span>© 2026 Newsletter Agent. All rights reserved.</span><br>
<span>Made with ❤️ by Goutam</span>
</div>

</td>
</tr>
</table>

</body>
</html>
"""