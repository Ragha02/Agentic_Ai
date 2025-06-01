# Building a Multi-Agent Content Creator with Ollama and CrewAI

This guide will walk you through setting up a multi-agent system to create content. We'll define three agents: a Researcher, a Writer, and an Editor, all powered by Ollama and orchestrated by CrewAI.

## 1. Prerequisites

Before we start, ensure you have the following installed:

- **Python 3.9+**: Make sure you have a compatible Python version.
- **Ollama**: Download and install Ollama from [ollama.com](https://ollama.com).
- **Required Python Libraries**: You'll need `crewai`, `langchain-ollama`, and `duckduckgo-search` (for web searching).

You can install the Python libraries using pip:

```bash
pip install crewai langchain-ollama duckduckgo-search==5.1.0
```

> **Note:** Pinning `duckduckgo-search` to 5.1.0 is recommended for compatibility with CrewAI.

## 2. Ollama Setup

After installing Ollama, you need to pull a language model. For this example, we'll use `llama3`. Open your terminal and run:

```bash
ollama pull llama3
```

Ensure Ollama is running in the background. You can verify this by checking your system's processes or trying to run `ollama run llama3 "Hello"`.

## 3. Define the Tools

Our agents will need a way to gather information. We'll use `DuckDuckGoSearchRun` as a web search tool.

```python
from crewai_tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# Initialize the DuckDuckGo Search Tool
duckduckgo_search_tool = DuckDuckGoSearchRun()

# Define a custom tool for web searching
@tool("Web Search Tool")
def web_search_tool(query: str) -> str:
    """Searches the web for the given query using DuckDuckGo."""
    return duckduckgo_search_tool.run(query)
```

## 4. Define the Agents

We'll define three agents, each with a specific role, goal, and backstory:

- **Researcher Agent**: Gathers and summarizes information
- **Writer Agent**: Drafts the initial content based on research
- **Editor Agent**: Refines the content, ensuring it's well-structured and in Markdown format

```python
from crewai import Agent
from langchain_community.llms import Ollama

# Initialize the Ollama LLM
ollama_llm = Ollama(model="llama3")

# Researcher Agent
researcher = Agent(
    role='Senior Research Analyst',
    goal='Discover and summarize relevant information on a given topic.',
    backstory=(
        "You are a seasoned research analyst with a knack for finding "
        "and distilling complex information into concise, actionable insights."
    ),
    llm=ollama_llm,
    tools=[web_search_tool], # Assign the web search tool
    verbose=True,
    allow_delegation=False
)

# Writer Agent
writer = Agent(
    role='Professional Content Writer',
    goal='Draft engaging and informative content based on research findings.',
    backstory=(
        "You are a creative and skilled content writer, capable of transforming "
        "raw information into compelling narratives and articles."
    ),
    llm=ollama_llm,
    verbose=True,
    allow_delegation=True # Can delegate to researcher if needed
)

# Editor Agent
editor = Agent(
    role='Senior Content Editor',
    goal='Review and refine content, ensuring high quality and correct markdown formatting.',
    backstory=(
        "You are a meticulous and experienced editor, with an eye for detail "
        "and a deep understanding of markdown syntax and content structure."
    ),
    llm=ollama_llm,
    verbose=True,
    allow_delegation=False
)
```

## 5. Define the Tasks

Next, we define the tasks for each agent. Tasks specify what the agent needs to do, what tools it might use, and what its expected output is.

```python
from crewai import Task

# Research Task
research_task = Task(
    description=(
        "Conduct comprehensive research on '{topic}'. "
        "Identify key concepts, statistics, and relevant examples. "
        "Summarize your findings into concise bullet points, focusing on "
        "meaningful insights that can be used for content creation."
    ),
    expected_output='A detailed summary of research findings in bullet points.',
    agent=researcher,
    tools=[web_search_tool]
)

# Writing Task
writing_task = Task(
    description=(
        "Based on the research findings provided, write a comprehensive article "
        "about '{topic}'. The article should be well-structured, engaging, "
        "and informative. Focus on explaining the key points and providing "
        "context. Do not include markdown formatting yet."
    ),
    expected_output='A well-written article draft without markdown formatting.',
    agent=writer,
    context=[research_task] # Writer uses the output of the research task
)

# Editing Task
editing_task = Task(
    description=(
        "Review the drafted article for clarity, coherence, and accuracy. "
        "Refine the language, correct any grammatical errors, and ensure "
        "the content flows naturally. Finally, format the entire article "
        "into a professional Markdown file, including appropriate headings, "
        "lists, and bold text where necessary. The final output MUST be a valid Markdown file."
    ),
    expected_output='A polished, well-formatted article in Markdown syntax.',
    agent=editor,
    context=[writing_task] # Editor uses the output of the writing task
)
```

## 6. Assemble the Crew

Finally, we assemble the agents and tasks into a Crew. The `process` parameter determines how tasks are executed (sequential means one after another).

```python
from crewai import Crew

# Assemble the Crew
content_crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    verbose=True # Set to True to see detailed logs
)
```

## 7. Run the Crew

To start the content creation process, execute the Crew with the desired topic.

```python
# Kick off the content creation process
topic = "The Impact of Artificial Intelligence on Modern Education"
result = content_crew.kickoff(inputs={'topic': topic})

print("\n\n########################")
print("## Here is the final content ##")
print("########################\n")
print(result)
```

## Conclusion

This setup allows the agents to collaborate effectively, with the researcher gathering information, the writer drafting the content, and the editor refining and formatting it into a final Markdown file. The multi-agent approach ensures that each aspect of content creation is handled by a specialized agent, resulting in higher quality output.

The system is flexible and can be customized for different types of content creation tasks by modifying the agent roles, goals, and task descriptions to suit your specific needs.
