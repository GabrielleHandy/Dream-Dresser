import os
import requests
import logging
from dotenv import load_dotenv

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
            temp = response['main']['temp']
            return temp
        except Exception as e:
            logger.error(f"Monica: 'I can't see outside! Error: {e}'")
            return None

    def validate_outfit(self, item_vibe, item_name):
        """The Guardrail: Monica decides if the outfit is appropriate."""
        temp = self.get_current_weather()
        if temp is None:
            return True, "Monica: 'I can't check the weather, so I'll trust you!'"

        # Monica's Rulebook (Logic)
        if temp < 50 and "tshirt" in item_name.lower():
            return False, f"Monica: 'It's {temp}°F! You cannot wear a tshirt. You'll catch a cold!'"
        
        if temp > 85 and "sweater" in item_name.lower():
            return False, f"Monica: 'It's {temp}°F! A sweater is a fashion disaster in this heat!'"

        return True, f"Monica: 'It's {temp}°F. The {item_name} is Monica-approved!'"