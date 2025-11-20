from agno.agent import Agent
from tools.serp_tools import get_search_tool

class ResearcherAgent(Agent):
    def __init__(self, model):
        super().__init__(
            name="Researcher",
            role="Senior Travel Researcher",
            instructions=[
                "You are a travel researcher. Use your tools to find REAL-TIME information.",
                "Research destination top attractions, current weather for the travel dates, and safety tips.",
                "Provide structured and concise information with source links."
            ],
            model=model,
            tools=[get_search_tool()], 
            markdown=True
        )