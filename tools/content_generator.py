import random

class TrevoContentGenerator:
    def __init__(self):
        # محاكاة لردود ذكية ومتنوعة تشبه نماذج الـ LLM
        self.templates = {
            "luxury": [
                "✨ Experience unparalleled elegance at {location}. Tailored exclusively for {audience}, this is where bespoke experiences meet timeless luxury. #TrevoElite",
                "🥂 Redefine your standards. {location} offers a pristine getaway for {audience} seeking the absolute finest in VIP hospitality. #LuxuryTravel"
            ],
            "adventure": [
                "⛰️ Answer the call of the wild in {location}! The ultimate adrenaline rush designed for {audience}. Gear up for the extraordinary. #TrevoAdventure",
                "🧗 Break your boundaries. {location} is the perfect playground for {audience} who crave thrill and raw nature. #ExploreMore"
            ],
            "budget": [
                "✈️ Maximize your experience, minimize your spend. {location} holds hidden gems perfect for {audience}. #TrevoSmart",
                "🎒 Authentic travel doesn't have to be expensive. Dive into the culture of {location} with our {audience} guide. #BudgetHacks"
            ]
        }

    def generate_copy(self, location, style="luxury", audience="Global Travelers"):
        # اختيار قالب عشوائي لتبدو المنصة كأنها تفكر في كل مرة
        style_templates = self.templates.get(style, self.templates["luxury"])
        template = random.choice(style_templates)
        return template.format(location=location, audience=audience)