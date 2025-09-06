#!/bin/bash

echo "🕘 SETTING UP PERMANENT DAILY AUTOMATION"
echo "========================================"

# Ensure the enhanced script is executable
chmod +x enhanced_daily_email.py

# Create logs directory
mkdir -p logs

# Set up the cron job with full path and logging
NIGELA_DIR="/Users/rushabhdoshi/Desktop/Nigela"
CRON_JOB="0 21 * * * cd $NIGELA_DIR && /usr/bin/python3 enhanced_daily_email.py >> $NIGELA_DIR/logs/daily_automation.log 2>&1"

# Remove any existing Nigela cron jobs
crontab -l 2>/dev/null | grep -v 'enhanced_daily_email.py' | grep -v 'src.cli email' | crontab -

# Add the new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job installed successfully!"
echo ""
echo "📋 Current cron jobs:"
crontab -l
echo ""
echo "🎯 AUTOMATION DETAILS:"
echo "   ⏰ Time: Every day at 9:00 PM"
echo "   📧 Recipients: palakbsanghavi@gmail.com + rushabh@machinecraft.org"
echo "   🔄 Variety: 2-week rotation system"
echo "   🎥 YouTube: Curated cooking channels"
echo "   📱 Format: Screenshot-ready for WhatsApp"
echo "   📝 Logs: $NIGELA_DIR/logs/daily_automation.log"
echo ""
echo "🚀 READY TO GO! First email tonight at 9 PM!"

