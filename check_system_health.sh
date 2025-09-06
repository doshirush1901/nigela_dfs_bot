#!/bin/bash

echo "🔍 NIGELA AI SYSTEM HEALTH CHECK"
echo "================================"
echo "Date: $(date)"
echo ""

echo "🔄 CRON JOB STATUS:"
crontab -l | grep "enhanced_daily_email_complete.py"
echo ""

echo "📧 RECENT EMAIL LOGS:"
if [ -f "logs/complete_nigella.log" ]; then
    echo "Last 10 entries:"
    tail -10 logs/complete_nigella.log
else
    echo "⚠️ No log file found yet"
fi
echo ""

echo "�� OAUTH TOKEN STATUS:"
if [ -f "gmail_token.json" ]; then
    echo "✅ OAuth token file exists"
    # Check if token is recent (modified within last 7 days)
    if [ $(find gmail_token.json -mtime -7) ]; then
        echo "✅ Token recently refreshed"
    else
        echo "⚠️ Token might need refresh soon"
    fi
else
    echo "❌ OAuth token missing!"
fi
echo ""

echo "📊 MEAL HISTORY STATUS:"
if [ -f "data/meal_history.json" ]; then
    echo "✅ Meal history tracking active"
    echo "Recent entries:"
    tail -5 data/meal_history.json
else
    echo "⚠️ No meal history found"
fi
echo ""

echo "🎭 SYSTEM COMPONENTS:"
echo "Core script: $([ -f "enhanced_daily_email_complete.py" ] && echo "✅ Present" || echo "❌ Missing")"
echo "Nigella persona: $([ -f "src/nigella_persona.py" ] && echo "✅ Present" || echo "❌ Missing")"
echo "YouTube curation: $([ -f "src/youtube_curated.py" ] && echo "✅ Present" || echo "❌ Missing")"
echo "Meal rotation: $([ -f "src/meal_rotation.py" ] && echo "✅ Present" || echo "❌ Missing")"

echo ""
echo "🎯 NEXT SCHEDULED EMAIL:"
echo "Tonight at 9:00 PM (21:00)"
echo ""
echo "✅ System health check complete!"
