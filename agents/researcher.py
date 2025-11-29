# researcher_agent.py
from agno.agent import Agent
from agno.models.google import Gemini

class ResearcherAgent(Agent):
    def __init__(self, model):
        super().__init__(
            name="Researcher",
            instructions=[
                "Research destination, top attractions, culture, and safety tips.",
                "Provide structured and concise information."
            ],
            model=model
        )
