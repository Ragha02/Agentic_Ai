# agents/research_agent.py
from crewai import Agent
from config.settings import AGENT_CONFIG

def create_research_agent(llm):
    """Create the research specialist agent"""
    return Agent(
        role="Research Specialist",
        goal="Gather comprehensive and accurate information on given topics",
        backstory=(
            "You are an expert researcher with years of experience in information "
            "gathering and analysis. You excel at finding key facts, statistics, "
            "and insights on any topic. You organize information clearly and "
            "identify the most important points for content creation."
        ),
        llm=llm,
        **AGENT_CONFIG
    )
