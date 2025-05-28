# agents/writer_agent.py
from crewai import Agent
from config.settings import AGENT_CONFIG

def create_writer_agent(llm):
    """Create the content writer agent"""
    return Agent(
        role="Content Writer",
        goal="Create engaging, well-structured, and informative content",
        backstory=(
            "You are a skilled content writer with expertise in creating "
            "compelling articles across various topics. You excel at turning "
            "research into readable, engaging content that captures the "
            "audience's attention while maintaining accuracy and clarity."
        ),
        llm=llm,
        **AGENT_CONFIG
    )
