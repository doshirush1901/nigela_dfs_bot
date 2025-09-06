#!/usr/bin/env python3
"""
Daily Feedback Email System
Sends structured feedback form at 10 PM for Google Doc completion
"""

import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, date, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def send_daily_feedback_form():
    """Send daily feedback form at 10 PM for Google Doc completion"""
    
    print("📋 Sending daily feedback form...")
    
    # Load OAuth
    creds = Credentials.from_authorized_user_file('gmail_token.json', ['https://www.googleapis.com/auth/gmail.send'])
    if not creds.valid:
        from google.auth.transport.requests import Request
        creds.refresh(Request())
    
    service = build('gmail', 'v1', credentials=creds)
    
    today = datetime.now()
    day_number = (today - datetime(2024, 9, 6)).days + 1  # Day 1 starts from Sept 6
    
    print(f"📅 Feedback form for Day {day_number}: {today.strftime('%A, %B %d, %Y')}")
    
    # Create structured feedback form for Google Doc
    feedback_form = f"""
NIGELA AI - DAILY FEEDBACK FORM
Day {day_number} - {today.strftime('%A, %B %d, %Y')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 EMAIL EXPERIENCE

1. Did tonight's menu email arrive on time (around 9 PM)?
   Answer: ________________

2. Rate Nigella's voice authenticity (1-5):
   British humor: ___
   Conversational warmth: ___  
   Food philosophy: ___

3. Cultural integration accuracy (1-5):
   Hindu/Jain calendar references: ___
   Mumbai market insights: ___
   Ayurvedic wisdom relevance: ___

4. What specific line or phrase made you smile today?
   Answer: ________________________________

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🍽️ MENU ASSESSMENT

5. Today's meal structure was: ________________
   (traditional thali / modern healthy / fusion / festival special)

6. Recipe practicality (1-5):
   Cooking time estimates: ___
   Ingredient availability: ___
   Recipe complexity: ___
   Instructions clarity: ___

7. Which recipes did your family actually cook today?
   Breakfast: ________________ (Rating: ___/5)
   Lunch: ________________ (Rating: ___/5)
   Dinner: ________________ (Rating: ___/5)
   Snacks: ________________ (Rating: ___/5)

8. Family reception (1-5):
   Cook found format helpful: ___
   Kids excited about meals: ___
   Parents satisfied with variety: ___

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎥 YOUTUBE INTEGRATION

9. How many YouTube links did you click? _____ out of _____

10. Most helpful video today:
    Recipe: ________________
    Channel: ________________
    Helpfulness (1-5): ___

11. Channel quality assessment (1-5):
    Traditional channels (Tarla Dalal, Ranveer Brar): ___
    Vegan specialists (Dr. Vegan, PlantYou, Sarah's): ___
    Video-recipe matching: ___

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 MOBILE & SHARING

12. Did you screenshot the menu table? Yes / No

13. Did you share it with your cook? Yes / No
    Cook's feedback: ________________

14. Mobile email format rating (1-5): ___
    Easy to read on phone: ___
    Screenshot quality: ___

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌱 CARBON-CONSCIOUS IMPACT

15. Plant-forward emphasis today (1-5): ___

16. Local/seasonal ingredients highlighted (1-5): ___

17. Did the menu help reduce food waste? Yes / No
    How: ________________

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 DAILY HIGHLIGHTS

18. What worked BRILLIANTLY today?
    1. ________________________________
    2. ________________________________
    3. ________________________________

19. What needs IMPROVEMENT?
    1. ________________________________
    2. ________________________________
    3. ________________________________

20. Kids' favorite meal today: ________________

21. Most challenging recipe: ________________

22. Surprise discovery: ________________

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 OVERALL DAY RATING

23. Email experience (1-5): ___
24. Menu quality (1-5): ___
25. Family satisfaction (1-5): ___
26. System reliability (1-5): ___

27. One sentence summary of today:
    ________________________________

28. Tomorrow's wish/suggestion:
    ________________________________

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNICAL NOTES (for system monitoring):
- Email delivery time: ______
- Any technical issues: ________________
- System suggestions: ________________

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Instructions: Copy this form to your Google Doc, fill in all answers, 
and after 7 days, share the complete document for AI analysis and 
system improvements.

Next feedback form arrives tomorrow at 10 PM!
    """
    
    # Create HTML version for better formatting
    html_content = f"""<html>
<body style="font-family: 'Courier New', monospace; max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9; color: #333; line-height: 1.4;">

<div style="text-align: center; background: #333; color: white; padding: 20px; margin-bottom: 20px;">
    <h1 style="margin: 0; font-size: 24px;">NIGELA AI - DAILY FEEDBACK</h1>
    <p style="margin: 8px 0 0 0; font-size: 14px;">Day {day_number} - {today.strftime('%A, %B %d, %Y')}</p>
    <p style="margin: 4px 0 0 0; font-size: 12px; opacity: 0.8;">Copy to Google Doc & Fill Out</p>
</div>

<div style="background: white; padding: 20px; border: 1px solid #ddd; font-size: 13px; white-space: pre-line;">
{feedback_form}
</div>

<div style="text-align: center; margin-top: 20px; padding: 15px; background: #e8f5e8; border-radius: 5px;">
    <p style="margin: 0; font-size: 12px; color: #666;">
        📋 <strong>Instructions:</strong> Copy this entire form to your Google Doc, fill in all answers throughout the week, 
        then share the completed document for AI analysis and system improvements.
    </p>
    <p style="margin: 8px 0 0 0; font-size: 11px; color: #999;">
        Next feedback form: Tomorrow at 10:00 PM
    </p>
</div>

</body>
</html>"""
    
    # Send the feedback form
    print("📤 Sending daily feedback form...")
    
    message = MIMEMultipart('alternative')
    message['to'] = 'rushabh@machinecraft.org'
    message['subject'] = f'Nigela Feedback Day {day_number} - Copy to Google Doc 📋'
    
    message.attach(MIMEText(feedback_form, 'plain'))
    message.attach(MIMEText(html_content, 'html'))
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_result = service.users().messages().send(
        userId='me',
        body={'raw': raw_message}
    ).execute()
    
    print(f"🎉 SUCCESS! Daily feedback form sent!")
    print(f"📧 Message ID: {send_result['id']}")
    print(f"📧 To: rushabh@machinecraft.org")
    print(f"📋 Day {day_number} feedback form ready for Google Doc")
    print("📝 Instructions: Copy form to Google Doc, fill daily, share after 7 days")

if __name__ == "__main__":
    send_daily_feedback_form()
