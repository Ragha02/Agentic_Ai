from crewai import Agent
from config.settings import AGENT_CONFIG

def create_editor_agent(llm):
    """Create the content editor agent"""
    return Agent(
        role="Content Editor",
        goal="Review and refine content for clarity, accuracy, and engagement",
        backstory=(
            "You are a meticulous editor with a keen eye for detail and "
            "excellent command of language. You improve content structure, "
            "fix grammatical errors, enhance readability, and ensure the "
            "content meets high quality standards for publication."
        ),
        llm=llm,
        **AGENT_CONFIG
    )