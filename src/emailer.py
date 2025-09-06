import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from .config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_FROM, EMAIL_TO, TIMEZONE
from .llm import nightly_email_copy

# Try to import Gmail API integration
try:
    from .gmail_auth import send_nigela_menu_email as gmail_send
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False

# Import enhanced email cards
try:
    from .email_cards import generate_complete_menu_email_html
    EMAIL_CARDS_AVAILABLE = True
except ImportError:
    EMAIL_CARDS_AVAILABLE = False

def render_plan_text(plan: dict) -> str:
    # fallback plain bullets if LLM not configured
    lines = []
    for meal, slots in plan.items():
        lines.append(f"\n{meal.upper()}")
        for slot, d in slots.items():
            lines.append(f" - {slot}: {d.name} ({d.cook_minutes}m)")
    return "\n".join(lines)

def send_menu_email(plan: dict, subject_date: str):
    if not (SMTP_HOST and SMTP_USER and SMTP_PASS and EMAIL_TO):
        print("⚠️ Email not configured; skipping send.")
        return False

    # Generate enhanced content with Pokémon-style cards
    try:
        body_text = nightly_email_copy(plan)
    except Exception:
        body_text = render_plan_text(plan)

    # Generate beautiful HTML email with recipe cards
    try:
        if EMAIL_CARDS_AVAILABLE:
            html_body = generate_complete_menu_email_html(plan, subject_date)
            print("🎨 Using enhanced Pokémon-style email cards!")
        else:
            html_body = f"<div style='font-family: Arial, sans-serif;'>{body_text.replace(chr(10), '<br>')}</div>"
    except Exception as e:
        print(f"⚠️ Card generation failed: {e}")
        html_body = f"<div style='font-family: Arial, sans-serif;'>{body_text.replace(chr(10), '<br>')}</div>"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Nigela • Complete Menu for {subject_date} 🍽️✨"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    msg.attach(MIMEText(body_text, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls(context=ctx)
        s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(EMAIL_FROM, [e.strip() for e in EMAIL_TO.split(",") if e.strip()], msg.as_string())
    print(f"📧 Enhanced menu email sent to {EMAIL_TO}")
    return True
