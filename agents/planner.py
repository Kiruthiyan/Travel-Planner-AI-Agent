from agno.agent import Agent

class PlannerAgent(Agent):
    def __init__(self, model):
        super().__init__(
            name="Planner",
            instructions=[
                "Create a day-by-day itinerary using research and hotel/restaurant info.",
                "Include flights, hotels, restaurants, and daily activities."
            ],
            model=model
        )
