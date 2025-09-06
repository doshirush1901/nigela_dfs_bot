#!/bin/bash

echo "📋 SETTING UP DAILY FEEDBACK EMAIL AUTOMATION"
echo "============================================"

# Set up feedback email cron job for 10 PM (1 hour after menu email)
NIGELA_DIR="/Users/rushabhdoshi/Desktop/Nigela"
FEEDBACK_CRON_JOB="0 22 * * * cd $NIGELA_DIR && /usr/bin/python3 daily_feedback_email.py >> $NIGELA_DIR/logs/feedback_daily.log 2>&1"

# Add the feedback cron job (keeping existing menu job)
(crontab -l 2>/dev/null; echo "$FEEDBACK_CRON_JOB") | crontab -

echo "✅ Daily feedback email automation set up!"
echo ""
echo "📋 Current cron jobs:"
crontab -l
echo ""
echo "🕘 DAILY SCHEDULE:"
echo "   9:00 PM: Menu email (to Palak + Rushabh)"
echo "   10:00 PM: Feedback form (to Rushabh for Google Doc)"
echo ""
echo "📝 WORKFLOW:"
echo "   1. Menu arrives at 9 PM"
echo "   2. Feedback form arrives at 10 PM" 
echo "   3. Copy form to Google Doc daily"
echo "   4. Fill out answers throughout the week"
echo "   5. After 7 days, share Google Doc for AI analysis"
echo ""
echo "🚀 Both automations now active!"

