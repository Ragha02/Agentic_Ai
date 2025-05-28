from config.llm_wrapper import CrewCompatibleLLM

# Default model and base URL for Ollama
DEFAULT_MODEL = "llama3.2:3b"
OLLAMA_BASE_URL = "http://localhost:11434"

# LLM model parameters
MODEL_CONFIG = {
    "temperature": 0.7,
    "num_predict": 512,
    "top_p": 0.9,
    "top_k": 40,
}

# Agent behavior configuration
AGENT_CONFIG = {
    "max_iter": 2,
    "verbose": True,
    "allow_delegation": False,
}

# Content generation requirements
CONTENT_CONFIG = {
    "min_word_count": 400,
    "max_word_count": 600,
    "research_sources": 5,
}

from config.llm_wrapper import CrewCompatibleLLM

def get_llm_config(model_name=None):
    model = model_name or DEFAULT_MODEL
    try:
        return CrewCompatibleLLM(model=model, base_url=OLLAMA_BASE_URL, **MODEL_CONFIG)
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        raise


def get_available_models():
    """Returns list of locally available Ollama models"""
    import subprocess
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error checking models: {e}"

# Optional alternative model configs
ALTERNATIVE_MODELS = {
    "phi3.5": {
        "model": "phi3.5:3.8b",
        "temperature": 0.6,
        "num_predict": 400,
    },
    "gemma2": {
        "model": "gemma2:2b",
        "temperature": 0.8,
        "num_predict": 300,
    },
    "llama3.2": {
        "model": "llama3.2:3b",
        "temperature": 0.7,
        "num_predict": 512,
    }
}
