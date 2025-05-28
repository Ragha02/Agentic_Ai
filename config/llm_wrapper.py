# config/llm_wrapper.py

from typing import Any, List, Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatResult
from langchain_community.chat_models import ChatOllama

class CrewCompatibleLLM(BaseChatModel):
    """A wrapper to make ChatOllama compatible with CrewAI"""

    def __init__(self, model: str, base_url: str, **kwargs: Any):
        # Don't register 'llm' as a dataclass field
        super().__init__()
        object.__setattr__(self, "llm", ChatOllama(model=model, base_url=base_url, **kwargs))

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> ChatResult:
        return self.llm._generate(messages, stop=stop, **kwargs)

    def invoke(self, messages: List[BaseMessage], **kwargs: Any) -> AIMessage:
        return self.llm.invoke(messages, **kwargs)

    @property
    def _llm_type(self) -> str:
        return "crew_compatible_ollama"
