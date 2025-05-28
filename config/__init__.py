# config/__init__.py
"""
Content Creation Pipeline Configuration

This module contains all configuration settings:
- Model configurations
- Agent settings
- Content parameters
- System settings
"""

from .settings import (
    get_llm_config,
    get_available_models,
    DEFAULT_MODEL,
    MODEL_CONFIG,
    AGENT_CONFIG,
    CONTENT_CONFIG,
    ALTERNATIVE_MODELS
)

__version__ = "1.0.0"
__author__ = "Content Pipeline Team"

# Make config easily importable
__all__ = [
    'get_llm_config',
    'get_available_models',
    'DEFAULT_MODEL',
    'MODEL_CONFIG',
    'AGENT_CONFIG',
    'CONTENT_CONFIG',
    'ALTERNATIVE_MODELS'
]

# Project metadata
PROJECT_NAME = "Content Creation Pipeline"
PROJECT_VERSION = "1.0.0"
SUPPORTED_MODELS = ["llama3.2:3b", "phi3.5:3.8b", "gemma2:2b"]

def get_project_info():
    """Get project information"""
    return {
        "name": PROJECT_NAME,
        "version": PROJECT_VERSION,
        "supported_models": SUPPORTED_MODELS,
        "default_model": DEFAULT_MODEL
    }