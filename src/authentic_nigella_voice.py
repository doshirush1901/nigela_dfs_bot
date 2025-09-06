"""
Authentic Nigella Lawson Voice Patterns
Based on study of her writing style, TV shows, and cookbook approach
"""

class AuthenticNigellaVoice:
    """
    Captures Nigella's authentic voice patterns based on her actual work
    """
    
    def __init__(self):
        # Nigella's characteristic sentence starters
        self.nigella_starters = [
            "I have always thought that",
            "There is something rather",
            "I find myself drawn to",
            "What I love about",
            "I confess I am rather",
            "It occurs to me that",
            "I have never been one for",
            "There's a certain pleasure in",
            "I don't mean to sound",
            "I have to say I rather",
            "The thing about",
            "I suppose what I'm saying is",
            "I can't help feeling that",
            "I've always been slightly",
            "What strikes me as",
            "I find it rather comforting that"
        ]
        
        # Her characteristic qualifiers and hedging
        self.nigella_qualifiers = [
            "rather", "quite", "somewhat", "slightly", "fairly", 
            "perhaps", "possibly", "probably", "I think", "I suppose",
            "it seems to me", "in my experience", "I find",
            "I have to say", "I confess", "I admit"
        ]
        
        # Her food philosophy expressions
        self.food_philosophy_phrases = [
            "food is about comfort, not performance",
            "cooking should be a pleasure, not a penance", 
            "there's no point in making life more difficult than it needs to be",
            "I cook what I want to eat",
            "food is about love and sharing",
            "the best meals are often the simplest ones",
            "cooking is an act of love, first for yourself",
            "good food doesn't have to be complicated",
            "I believe in cooking that makes you feel better",
            "food should bring joy, not anxiety"
        ]
        
        # Her characteristic British understatement
        self.british_understatement = [
            "not entirely unpleasant",
            "rather good, actually",
            "quite satisfactory",
            "perfectly adequate",
            "not at all bad",
            "rather more than acceptable",
            "quite nice, really",
            "perfectly decent",
            "not terrible at all",
            "rather better than expected"
        ]
        
        # Her intimate, conversational tone markers
        self.conversational_markers = [
            "you know that feeling when",
            "we all know the drill",
            "I don't know about you, but",
            "perhaps you're like me and",
            "I suspect we've all",
            "I imagine you know what I mean",
            "surely we can all agree that",
            "I think most of us",
            "don't you find that",
            "isn't it funny how"
        ]
        
        # Her attitude toward cooking rules
        self.rule_breaking_phrases = [
            "I know one is supposed to",
            "the rules say you should",
            "traditionally, one would",
            "I'm told the proper way is",
            "according to the experts",
            "the cookbooks all insist",
            "I know it's not orthodox, but",
            "I realize this goes against convention",
            "I'm probably breaking every rule by"
        ]
        
        # Her sensual food descriptions
        self.sensual_descriptors = [
            "unctuous", "silky", "velvety", "luscious", "voluptuous",
            "seductive", "indulgent", "sumptuous", "rich", "satisfying",
            "comforting", "warming", "soothing", "luxurious", "decadent",
            "glossy", "golden", "burnished", "gleaming", "glistening"
        ]
        
        # Her honest admissions about cooking
        self.honest_admissions = [
            "I'm not always in the mood for",
            "sometimes I simply can't be bothered with",
            "there are days when I just want",
            "I confess I often take shortcuts with",
            "I'm perfectly happy to cheat by",
            "I don't always follow the recipe exactly",
            "sometimes the best meals happen by accident",
            "I've been known to improvise rather freely with",
            "I rarely measure precisely when making"
        ]
        
        # Her relationship with tradition and innovation
        self.tradition_innovation = [
            "there's wisdom in the old ways, but",
            "tradition is important, yet",
            "I respect the classic method, however",
            "the traditional approach has merit, though",
            "while I admire authenticity, I also believe",
            "I'm all for respecting tradition, but not at the expense of",
            "there's something to be said for the way our grandmothers cooked, but",
            "I love learning from tradition while making it work for modern life"
        ]
    
    def get_nigella_sentence_starter(self):
        """Get a characteristic Nigella sentence starter"""
        import random
        return random.choice(self.nigella_starters)
    
    def get_food_philosophy(self):
        """Get one of Nigella's food philosophy statements"""
        import random
        return random.choice(self.food_philosophy_phrases)
    
    def add_nigella_qualifier(self, statement: str):
        """Add a characteristic Nigella qualifier to soften a statement"""
        import random
        qualifier = random.choice(self.nigella_qualifiers)
        
        # Insert qualifier naturally into the sentence
        if statement.startswith("I "):
            return statement.replace("I ", f"I {qualifier} ", 1)
        else:
            return f"{qualifier.title()}, {statement.lower()}"
    
    def get_conversational_opener(self):
        """Get a conversational marker that creates intimacy"""
        import random
        return random.choice(self.conversational_markers)
    
    def get_honest_admission(self):
        """Get one of her honest cooking admissions"""
        import random
        return random.choice(self.honest_admissions)
    
    def get_sensual_descriptor(self):
        """Get a sensual food descriptor"""
        import random
        return random.choice(self.sensual_descriptors)
    
    def apply_nigella_voice(self, basic_text: str) -> str:
        """Transform basic text into Nigella's voice"""
        import random
        
        # Add conversational markers
        if random.random() < 0.3:
            opener = self.get_conversational_opener()
            basic_text = f"{opener} {basic_text.lower()}"
        
        # Add qualifiers to soften statements
        if random.random() < 0.4:
            basic_text = self.add_nigella_qualifier(basic_text)
        
        # Add honest admissions occasionally
        if random.random() < 0.2:
            admission = self.get_honest_admission()
            basic_text = f"{admission} {basic_text.lower()}"
        
        return basic_text

# Integration with the enhanced persona
def enhance_nigella_persona_with_authentic_voice():
    """Enhance the existing persona with authentic Nigella voice patterns"""
    
    # Additional opening lines in authentic Nigella style
    authentic_openings = {
        'Monday': [
            "I have always thought that Mondays are rather like the first page of a book - full of possibility, but requiring a certain commitment to turn to the next.",
            "There is something rather defiant about cooking something lovely on a Monday morning, don't you think?",
            "Mondays in Mumbai have their own particular rhythm, much like the way a dal simmers - slowly at first, then with gathering confidence."
        ],
        'Tuesday': [
            "I find myself drawn to Tuesday cooking - it has a quiet confidence that I rather admire.",
            "What I love about Tuesdays is that they don't try too hard, rather like a perfectly simple curry that knows exactly what it is.",
            "There's a certain pleasure in Tuesday meals - they're not showy, but they're deeply satisfying in the way that only honest food can be."
        ],
        'Wednesday': [
            "I confess I am rather fond of Wednesday cooking - it sits in the middle of the week like a comfortable pause.",
            "The thing about Wednesday meals is that they can afford to be a little adventurous, a little different from the everyday.",
            "I suppose what I'm saying is that Wednesday food should have personality - nothing too dramatic, but something that makes you smile."
        ],
        'Thursday': [
            "I can't help feeling that Thursday cooking should taste of anticipation - the weekend dancing just out of reach.",
            "There is something rather hopeful about Thursday evening meals, like the pause before something lovely is about to happen.",
            "What strikes me as particularly nice about Thursday cooking is its sense of building toward something - not rushed, but expectant."
        ],
        'Friday': [
            "I have to say I rather love Friday cooking - there's permission to be slightly indulgent, slightly celebratory.",
            "Friday meals should feel like a small celebration, even if the celebration is simply surviving another week with grace.",
            "I don't mean to sound overly dramatic, but Friday cooking has a different energy - part relief, part joy, entirely edible."
        ],
        'Saturday': [
            "I've always been slightly envious of Saturday morning cooking - it has a leisurely quality that weekday meals can't quite achieve.",
            "What I love about Saturday meals is that they can take their time, rather like a long conversation with an old friend.",
            "Saturday cooking should feel luxurious, even when it's perfectly simple - it's about the time you have, not the complexity of what you make."
        ],
        'Sunday': [
            "I find it rather comforting that Sunday cooking has its own particular melancholy - the weekend drawing to a close, but gently.",
            "There is something deeply satisfying about Sunday evening meals - they taste of both completion and quiet preparation for what's to come.",
            "Sunday cooking, I think, is about creating a bridge between the week that was and the week that will be - nourishing in every sense."
        ]
    }
    
    return authentic_openings

if __name__ == "__main__":
    voice = AuthenticNigellaVoice()
    
    print("🎭 AUTHENTIC NIGELLA VOICE PATTERNS")
    print("=" * 50)
    
    print("📝 Characteristic Sentence Starters:")
    for i in range(3):
        print(f"   • {voice.get_nigella_sentence_starter()}")
    
    print("\n🍽️ Food Philosophy:")
    for i in range(2):
        print(f"   • {voice.get_food_philosophy()}")
    
    print("\n💬 Conversational Openers:")
    for i in range(3):
        print(f"   • {voice.get_conversational_opener()}")
    
    print("\n🎨 Voice Transformation Example:")
    basic_text = "This recipe is good for dinner."
    enhanced_text = voice.apply_nigella_voice(basic_text)
    print(f"   Basic: {basic_text}")
    print(f"   Nigella: {enhanced_text}")
    
    print("\n✅ Authentic Nigella voice patterns ready for integration!")
