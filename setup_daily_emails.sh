#!/bin/bash

# Nigela Daily Email Automation Setup Script
# This script sets up automatic daily menu emails at 9 PM

echo "⏰ SETTING UP NIGELA DAILY EMAIL AUTOMATION"
echo "=========================================="

# Get current directory
NIGELA_DIR="/Users/rushabhdoshi/Desktop/Nigela"
PYTHON_PATH="/usr/bin/python3"

# Create logs directory
mkdir -p "$NIGELA_DIR/logs"

# Create the cron job entry
CRON_JOB="0 21 * * * cd $NIGELA_DIR && $PYTHON_PATH -m src.cli email --for tomorrow >> $NIGELA_DIR/logs/daily_email.log 2>&1"

echo "📝 Cron job to be added:"
echo "$CRON_JOB"
echo

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "src.cli email"; then
    echo "⚠️  Nigela email cron job already exists!"
    echo "📋 Current cron jobs:"
    crontab -l | grep -E "(Nigela|src.cli)"
else
    echo "➕ Adding cron job..."
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    
    if [ $? -eq 0 ]; then
        echo "✅ SUCCESS! Daily email automation set up!"
        echo
        echo "📧 WHAT HAPPENS NOW:"
        echo "• Every day at 9:00 PM"
        echo "• Nigela will automatically generate tomorrow's menu"
        echo "• Beautiful email sent to palakbsanghavi@gmail.com"
        echo "• Logs saved to: $NIGELA_DIR/logs/daily_email.log"
        echo
        echo "🔍 To check cron job:"
        echo "crontab -l | grep Nigela"
        echo
        echo "🗑️ To remove automation:"
        echo "crontab -l | grep -v 'src.cli email' | crontab -"
    else
        echo "❌ Failed to add cron job"
        echo "💡 You may need to manually add it"
    fi
fi

echo
echo "🎯 MANUAL TEST COMMANDS:"
echo "# Send tomorrow's menu now:"
echo "python3 -m src.cli email --for tomorrow"
echo
echo "# Check logs:"
echo "tail -f logs/daily_email.log"

echo
echo "✨ Nigela is now your daily cooking assistant!"
