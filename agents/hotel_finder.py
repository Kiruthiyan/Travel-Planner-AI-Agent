from agno.agent import Agent

class HotelFinderAgent(Agent):
    def __init__(self, model):
        super().__init__(
            name="HotelFinder",
            instructions=[
                "Search for best hotels and restaurants based on destination, budget, and hotel rating.",
                "Provide names, ratings, and locations."
            ],
            model=model
        )
