from agno.agent import Agent
from tools.serp_tools import get_search_tool

class HotelFinderAgent(Agent):
    def __init__(self, model):
        super().__init__(
            name="HotelFinder",
            role="Hospitality Expert",
            instructions=[
                "Search for currently operating hotels and restaurants matching the user's budget.",
                "Do not invent prices. Find real options with current ratings.",
                "Include the address or neighborhood for every recommendation."
            ],
            model=model,
            tools=[get_search_tool()], # <--- CONNECTS TO INTERNET
            markdown=True
        )