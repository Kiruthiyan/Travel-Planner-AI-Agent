from agno.agent import Agent

class PlannerAgent(Agent):
    def __init__(self, model):
        super().__init__(
            name="Planner",
            role="Chief Travel Architect",
            instructions=[
                "Create a highly readable, day-by-day itinerary.",
                "FORMATTING RULES:",
                "1. Use emojis for every section header (e.g., 🌅 Morning, 🍽️ Lunch).",
                "2. Do NOT write long paragraphs. Use bullet points.",
                "3. Bold key locations and restaurant names.",
                "4. Add a '💰 Estimated Daily Cost' summary at the end of each day.",
                "5. Start with a 'Trip Overview' summary card.",
                "6. Use '### Day X: Title' for daily headers so they are distinct."
            ],
            model=model,
            markdown=True
        )