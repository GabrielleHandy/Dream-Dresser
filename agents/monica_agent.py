import os
import requests
import logging
from dotenv import load_dotenv
from utils.grammarUtility import get_label_agreement # New Import

logger = logging.getLogger("MonicaRuleAgent")

class MonicaRuleAgent:
    def __init__(self, city="Winston-Salem"):
        load_dotenv()
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.city = city

    def get_current_weather(self):
        """Fetch real-time temperature."""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=imperial"
            response = requests.get(url).json()
            return response['main']['temp']
        except Exception as e:
            logger.error(f"Monica: 'I can't see outside! Error: {e}'")
            return None

    def validate_outfit(self, item_vibe, item_name):
        """Monica decides if the outfit is appropriate."""
        temp = self.get_current_weather()
        grammar = get_label_agreement(item_name) # Fetch grammar bits
        
        if temp is None:
            return True, f"Monica: 'I can't check the weather, so I'll trust that {grammar['selector']} {item_name} {grammar['verb']} okay!'"

        # Monica's Rulebook with corrected grammar
        if temp < 50 and "tshirt" in item_name.lower():
            return False, f"Monica: 'It's {temp}°F! You cannot wear {grammar['selector']} {item_name}. You'll catch a cold!'"
        
        if temp > 85 and "sweater" in item_name.lower():
            return False, f"Monica: 'It's {temp}°F! {grammar['selector'].capitalize()} {item_name} {grammar['verb']} a fashion disaster in this heat!'"

        return True, f"Monica: 'It's {temp}°F. {grammar['selector'].capitalize()} {item_name} {grammar['verb']} Monica-approved!'"