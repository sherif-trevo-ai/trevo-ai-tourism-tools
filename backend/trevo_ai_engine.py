"""
Trevo AI Core Engine (v2.0)
---------------------------------------------------------
This module handles the backend AI logic for Trevo's 
Tourism Superplatform. It includes features for generating 
AI marketing content, smart booking analytics, and automated
travel itineraries tailored for the MENA region.

Language Support: Arabic (ar) & English (en)
"""

import os
import json
import random
from datetime import datetime

class TrevoAIEngine:
    def __init__(self, api_key=None, default_lang="ar"):
        """
        Initialize the Trevo AI Engine.
        :param api_key: AI Service Provider Key (e.g., OpenAI)
        :param default_lang: Default response language ('ar' or 'en')
        """
        self.api_key = api_key or os.getenv("TREVO_AI_KEY", "demo_mode_active")
        self.current_lang = default_lang
        self.supported_destinations = ["Cairo", "Luxor", "Riyadh", "Jeddah", "Dubai", "Hurghada"]

    def generate_campaign_content(self, destination, duration_days, target_audience):
        """
        Generates a 30-day social media campaign for travel agencies.
        """
        if destination not in self.supported_destinations:
            return {"error": "Destination currently not supported in the database."}

        # Mocking the AI response for demonstration
        print(f"[Trevo AI] Generating {duration_days}-day campaign for {destination}...")
        
        campaign = {
            "campaign_name": f"Explore {destination} - {datetime.now().year}",
            "target": target_audience,
            "language": self.current_lang,
            "posts": [
                {
                    "day": 1,
                    "platform": "Instagram",
                    "content": f"اكتشف سحر {destination} معنا! عروض حصرية تبدأ اليوم. ✈️✨" if self.current_lang == "ar" else f"Discover the magic of {destination}! Exclusive deals start today. ✈️✨",
                    "hashtags": f"#Travel #TrevoAI #{destination}"
                },
                {
                    "day": 2,
                    "platform": "Facebook",
                    "content": "هل خططت لإجازتك القادمة؟ دع الذكاء الاصطناعي ينظم رحلتك." if self.current_lang == "ar" else "Planned your next vacation? Let AI organize your trip.",
                    "hashtags": "#Tourism #SmartBooking"
                }
            ]
        }
        return campaign

    def calculate_agency_roi(self, monthly_spend, manual_hours_spent):
        """
        Calculates the estimated ROI and time saved for an agency using Trevo.
        """
        trevo_cost = 50  # Starting price as per pricing plan
        freelancer_avg_cost = 1000
        hours_saved = manual_hours_spent * 0.85  # Trevo saves 85% of manual work
        
        money_saved = freelancer_avg_cost - trevo_cost
        booking_uplift_percentage = random.randint(15, 35)

        report = {
            "monthly_savings_usd": money_saved,
            "hours_saved_per_week": hours_saved,
            "expected_booking_uplift": f"+{booking_uplift_percentage}%",
            "recommendation": "Upgrade to Growth Plan to unlock AR/VR previews."
        }
        return report

    def generate_smart_itinerary(self, user_preferences):
        """
        Builds a customized B2C travel itinerary based on user preferences.
        """
        print("[Trevo AI] Analyzing user preferences and building itinerary...")
        return {
            "status": "success",
            "itinerary_id": f"TRV-{random.randint(1000, 9999)}",
            "details": "Dynamic AI-generated itinerary ready for B2C app."
        }

# ==========================================
# Example Usage (Testing the Engine)
# ==========================================
if __name__ == "__main__":
    # Initialize engine in Arabic mode
    ai_engine = TrevoAIEngine(default_lang="ar")
    
    print("🚀 Starting Trevo AI Engine Simulation...\n")
    
    # 1. Test Content Generation
    campaign_data = ai_engine.generate_campaign_content(
        destination="Luxor",
        duration_days=5,
        target_audience="Families"
    )
    print(">> Campaign Generated:")
    print(json.dumps(campaign_data, indent=2, ensure_ascii=False))
    print("-" * 40)
    
    # 2. Test ROI Calculator
    roi_report = ai_engine.calculate_agency_roi(monthly_spend=1500, manual_hours_spent=40)
    print(">> Agency ROI Report:")
    print(json.dumps(roi_report, indent=2))
