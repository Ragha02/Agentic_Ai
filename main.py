#!/usr/bin/env python3
"""
Content Creation Pipeline - Main Entry Point
Multi-Agent System using CrewAI with Ollama models
"""

import os
from datetime import datetime
from crewai import Crew, Process
from agents.research_agent import create_research_agent
from agents.writer_agent import create_writer_agent
from agents.editor_agent import create_editor_agent
from tools.search_tools import get_search_context
from config.settings import get_llm_config


def create_content_pipeline(topic: str):
    """Create and execute the content creation pipeline"""

    print(f"\n🚀 Starting Content Creation Pipeline")
    print(f"📝 Topic: {topic}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Get LLM configuration
    llm = get_llm_config()

    # Get search context for the topic
    search_context = get_search_context(topic)

    # Create agents
    print("\n👥 Initializing Agents...")
    research_agent = create_research_agent(llm)
    writer_agent = create_writer_agent(llm)
    editor_agent = create_editor_agent(llm)

    # Create tasks
    print("📋 Creating Tasks...")
    from crewai import Task

    research_task = Task(
        description=(
            f"Research the topic: '{topic}'\n"
            f"Here's some web search information to help:\n"
            f"{search_context}\n\n"
            "Based on the above information and your knowledge, provide:\n"
            "- Key facts and statistics\n"
            "- Main concepts and definitions\n"
            "- Current trends or developments\n"
            "- 3-5 important points to cover\n"
            "Keep research concise but comprehensive."
        ),
        agent=research_agent,
        expected_output="A structured research report with key findings and main points"
    )

    writing_task = Task(
        description=(
            f"Using the research provided, write a 400-600 word article about '{topic}'.\n"
            "Requirements:\n"
            "- Engaging introduction\n"
            "- Clear, logical structure\n"
            "- Include key facts from research\n"
            "- Conversational but informative tone\n"
            "- Strong conclusion"
        ),
        agent=writer_agent,
        expected_output="A well-structured 400-600 word article",
        context=[research_task]
    )

    editing_task = Task(
        description=(
            "Edit and refine the article to improve:\n"
            "- Grammar and spelling\n"
            "- Sentence flow and readability\n"
            "- Structure and organization\n"
            "- Clarity of explanations\n"
            "- Overall engagement\n"
            "Provide the final polished version."
        ),
        agent=editor_agent,
        expected_output="A polished, publication-ready article",
        context=[writing_task]
    )

    # Create and run the crew
    print("🚁 Assembling Crew...")
    crew = Crew(
        agents=[research_agent, writer_agent, editor_agent],
        tasks=[research_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=True,
        memory=False,
    )

    print("\n🎬 Starting Content Creation Process...")
    result = crew.kickoff()

    return result


def save_content(topic: str, content: str):
    """Save the generated content to a file"""
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_').lower()
    filename = f"output/content_{safe_topic}_{timestamp}.txt"

    # Save content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Content Creation Pipeline Output\n")
        f.write(f"Topic: {topic}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(str(content))

    return filename


def main():
    """Main function"""
    print("🎯 Content Creation Pipeline - Multi-Agent System")
    print("=" * 60)

    # Example topics
    sample_topics = [
        "The Future of Renewable Energy",
        "Benefits of Remote Work",
        "Introduction to Machine Learning",
        "Sustainable Urban Gardening",
        "Digital Privacy in 2025"
    ]

    print("\n📋 Sample Topics:")
    for i, topic in enumerate(sample_topics, 1):
        print(f"  {i}. {topic}")

    # Get topic from user
    topic = input("\n✏️  Enter a topic for content creation (or press Enter for default): ").strip()
    if not topic:
        topic = sample_topics[0]  # Default topic
        print(f"Using default topic: {topic}")

    try:
        # Create content
        final_result = create_content_pipeline(topic)

        # Display results
        print("\n" + "=" * 60)
        print("🎉 FINAL CONTENT:")
        print("=" * 60)
        print(final_result)

        # Save to file
        filename = save_content(topic, final_result)
        print(f"\n💾 Content saved to: {filename}")

        print("\n✅ Content creation pipeline completed successfully!")

    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Check if model is available: ollama list")
        print("3. Pull the model if needed: ollama pull llama3.2:3b")


if __name__ == "__main__":
    main()