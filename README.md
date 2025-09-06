# Nigela AI - Advanced Cooking Assistant

A sophisticated AI-powered cooking assistant that combines British culinary wit (Nigella Lawson style) with Indian spiritual wisdom, Ayurvedic knowledge, and modern nutrition science.

## Features

### 🎭 Authentic Nigella Lawson Persona
- British dry humor and conversational intimacy
- Food philosophy woven throughout
- Honest admissions and gentle guidance

### 📅 Cultural Intelligence
- Hindu/Jain calendar integration
- Festival-appropriate food suggestions
- Ayurvedic seasonal wisdom
- Mumbai market seasonality

### 🎥 Enhanced YouTube Curation
- Traditional channels: Happy Pear, Chef Ranveer Brar, Tarla Dalal
- Vegan specialists: Dr. Vegan, Sarah's Vegan Kitchen, PlantYou
- Smart recipe-to-channel matching

### 🔄 Advanced Meal Planning
- 2-week variety rotation (no repeats)
- Multiple meal structures by day
- Jain-friendly options
- Nutrition tracking for families

### 📧 Daily Automation
- Sends at 9 PM daily via Gmail API
- OAuth secure authentication
- Mobile-optimized format
- Screenshot-ready for sharing with cook

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up Gmail OAuth:
   - Create Google Cloud project
   - Enable Gmail API
   - Download credentials as `gmail_token.json`

3. Initialize data:
   ```bash
   python3 -m src.bootstrap
   ```

4. Test the system:
   ```bash
   python3 enhanced_daily_email_complete.py
   ```

## Daily Automation

The system runs automatically every day at 9 PM via cron:

```bash
0 21 * * * cd /path/to/Nigela && python3 enhanced_daily_email_complete.py
```

## File Structure

```
Nigela/
├── src/                          # Core modules
│   ├── authentic_nigella_voice.py # Voice patterns
│   ├── nigella_persona.py        # Cultural integration
│   ├── youtube_curated.py        # Video curation
│   ├── meal_rotation.py          # Variety system
│   ├── cookbook_collector.py     # Recipe sourcing
│   └── ...
├── data/                         # Recipe database
├── library/                      # Cookbook collection
├── logs/                         # Automation logs
└── enhanced_daily_email_complete.py # Main automation
```

## Key Components

- **Meal Rotation**: 2-week variety cycle with no repeats
- **Cultural Calendar**: Hindu/Jain festivals and food wisdom
- **Ayurvedic Integration**: Seasonal doshas and food qualities
- **Mumbai Markets**: Local seasonality and availability
- **YouTube Curation**: 13+ premium cooking channels
- **Voice Authenticity**: Based on Nigella Lawson's actual patterns

## License

Personal use project - Sophisticated AI cooking assistant for daily meal planning.
