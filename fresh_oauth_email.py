#!/usr/bin/env python3
"""
Fresh OAuth Email Sender for Nigela
Clean implementation using new credentials
"""

import os
import json
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class FreshGmailSender:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.token_file = "fresh_gmail_token.json"
        self.service = None
        
    def authenticate(self):
        """Fresh OAuth authentication"""
        print(f"🔐 Starting fresh OAuth with: {self.credentials_file}")
        
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(f"Credentials file not found: {self.credentials_file}")
        
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_file):
            print("📱 Found existing token, checking validity...")
            try:
                creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
            except Exception as e:
                print(f"⚠️ Token load error: {e}")
                creds = None
        
        # If no valid credentials, start fresh OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Attempting token refresh...")
                try:
                    creds.refresh(Request())
                    print("✅ Token refreshed successfully!")
                except Exception as e:
                    print(f"⚠️ Token refresh failed: {e}")
                    creds = None
            
            if not creds:
                print("🌐 Starting fresh OAuth flow...")
                print("📱 Browser will open for authorization...")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                
                # Run the OAuth flow with automatic browser opening
                creds = flow.run_local_server(
                    port=0,
                    open_browser=True,
                    prompt='consent',
                    access_type='offline'
                )
                print("✅ OAuth flow completed successfully!")
            
            # Save credentials for future use
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
            print(f"💾 Fresh credentials saved to: {self.token_file}")
        else:
            print("✅ Using existing valid credentials!")
        
        # Build Gmail service
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            print("📧 Gmail service initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Gmail service initialization failed: {e}")
            return False
    
    def send_enhanced_email(self, to_email, subject, text_content, html_content):
        """Send email via Gmail API"""
        if not self.service:
            raise RuntimeError("Gmail service not initialized. Call authenticate() first.")
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['to'] = to_email
            message['subject'] = subject
            
            # Add text and HTML parts
            message.attach(MIMEText(text_content, 'plain'))
            message.attach(MIMEText(html_content, 'html'))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send via Gmail API
            send_result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print(f"🎉 SUCCESS! Email sent to {to_email}")
            print(f"📧 Gmail Message ID: {send_result['id']}")
            return send_result['id']
            
        except HttpError as error:
            print(f"❌ Gmail API error: {error}")
            return None
        except Exception as error:
            print(f"❌ Email sending error: {error}")
            return None

def main():
    print("🚀 FRESH OAUTH EMAIL SENDER FOR NIGELA")
    print("=" * 50)
    
    # Use the new credentials file
    credentials_file = "client_secret_29686905270-kpilc6tvksf2dga3gmrd6lltld3qhqcv.apps.googleusercontent.com.json"
    
    # Initialize Gmail sender
    gmail = FreshGmailSender(credentials_file)
    
    # Authenticate
    if not gmail.authenticate():
        print("❌ Authentication failed")
        return False
    
    # Create enhanced email content
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nigela Fresh OAuth Success</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif; background: #ffffff; margin: 0; padding: 20px; color: #000000;">
    <div style="max-width: 340px; margin: 0 auto;">
        <div style="text-align: center; padding: 40px 20px; border-bottom: 1px solid #000000; margin-bottom: 32px;">
            <h1 style="margin: 0; font-size: 24px; font-weight: 400; letter-spacing: 2px; color: #000000;">NIGELA</h1>
            <p style="margin: 8px 0 0 0; font-size: 14px; color: #666666; font-weight: 300; letter-spacing: 1px;">FRESH OAUTH SUCCESS!</p>
            <p style="margin: 4px 0 0 0; font-size: 12px; color: #999999; font-weight: 300;">Enhanced Email System Authenticated</p>
        </div>
        
        <div style="border: 1px solid #000000; background: white; margin-bottom: 24px;">
            <div style="background: #000000; color: white; padding: 16px; text-align: center;">
                <h2 style="margin: 0; font-size: 16px; font-weight: 500; letter-spacing: 1px;">AUTHENTICATION COMPLETE</h2>
            </div>
            
            <div style="padding: 16px;">
                <p style="margin: 0 0 16px 0; font-size: 14px; color: #333;">Hi Palak! 👋</p>
                <p style="margin: 0 0 16px 0; font-size: 13px; color: #666; line-height: 1.5;">🎉 Fantastic! Your Nigela AI cooking assistant is now properly authenticated with fresh OAuth credentials and ready to send you stunning daily meal plans!</p>
                
                <div style="background: #f8f8f8; padding: 16px; border: 1px solid #e0e0e0; margin: 16px 0;">
                    <h4 style="margin: 0 0 12px 0; font-size: 13px; font-weight: 600; color: #000; letter-spacing: 0.5px;">✨ ENHANCED FEATURES READY</h4>
                    <ul style="margin: 0; padding-left: 16px; font-size: 12px; color: #333; line-height: 1.6;">
                        <li style="margin-bottom: 4px;"><strong>Maruko Labs Design:</strong> Clean black & white aesthetic</li>
                        <li style="margin-bottom: 4px;"><strong>Smart Filtering:</strong> Recipe cards for complex dishes only</li>
                        <li style="margin-bottom: 4px;"><strong>Health Analysis:</strong> Complete nutrition with health scores</li>
                        <li style="margin-bottom: 4px;"><strong>Prep Instructions:</strong> What to soak tonight</li>
                        <li style="margin-bottom: 4px;"><strong>Special Comments:</strong> Cooking tips & health benefits</li>
                        <li style="margin-bottom: 4px;"><strong>Grocery Management:</strong> Fridge check + Blinkit delivery</li>
                    </ul>
                </div>
                
                <div style="background: #000000; color: white; padding: 16px; text-align: center; margin: 16px 0;">
                    <p style="margin: 0; font-size: 13px; letter-spacing: 0.5px; font-weight: 600;">DAILY EMAILS START TOMORROW AT 9 PM</p>
                    <p style="margin: 4px 0 0 0; font-size: 11px; opacity: 0.8;">Complete 5-meal health plans with iPhone-optimized design</p>
                </div>
                
                <p style="margin: 0; text-align: center; font-style: italic; color: #666; font-size: 14px;">With love from your kitchen,<br>Nigela ⚫⚪✨</p>
            </div>
        </div>
        
        <div style="text-align: center; padding: 16px 0; border-top: 1px solid #000000;">
            <p style="margin: 0; font-size: 11px; color: #666; font-weight: 300; letter-spacing: 0.5px;">FRESH OAUTH AUTHENTICATION COMPLETE</p>
            <p style="margin: 4px 0 0 0; font-size: 9px; color: #999; letter-spacing: 0.5px;">GENERATED BY NIGELA AI • POWERED BY OPENAI</p>
        </div>
    </div>
</body>
</html>"""

    text_content = """NIGELA FRESH OAUTH SUCCESS!

Hi Palak!

🎉 Your Nigela AI cooking assistant is now properly authenticated with fresh OAuth credentials!

✨ ENHANCED FEATURES READY:
• Maruko Labs Design: Clean black & white aesthetic
• Smart Filtering: Recipe cards for complex dishes only  
• Health Analysis: Complete nutrition with health scores
• Prep Instructions: What to soak tonight
• Special Comments: Cooking tips & health benefits
• Grocery Management: Fridge check + Blinkit delivery

📧 DAILY EMAILS START TOMORROW AT 9 PM
Complete 5-meal health plans with iPhone-optimized design

With love from your kitchen,
Nigela ⚫⚪✨

Fresh OAuth Authentication Complete
Generated by Nigela AI • Powered by OpenAI"""
    
    # Send the email
    message_id = gmail.send_enhanced_email(
        "palakbsanghavi@gmail.com",
        "Nigela Fresh OAuth Success • Enhanced Daily Emails Ready! ⚫⚪",
        text_content,
        html_content
    )
    
    if message_id:
        print("🎊 COMPLETE SUCCESS!")
        print("📱 Palak will receive the beautiful enhanced email")
        print("✅ Daily automation is now ready for 9 PM emails")
        print("🔄 OAuth authentication working perfectly")
        return True
    else:
        print("❌ Email sending failed")
        return False

if __name__ == "__main__":
    main()
