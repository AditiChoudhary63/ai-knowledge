from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel
def get_llm(
    provider: str = "openai",
    model: str | None = None,
    temperature: float = 0.2,
) -> BaseChatModel:
    """
    Returns a provider-agnostic LangChain LLM.
    API keys are read from environment variables.
    """

    if provider == "openai":
        return ChatOpenAI(
            model=model or "gpt-4o-mini",
            temperature=temperature,
        )

    if provider == "groq":
        return ChatGroq(
            model=model or "llama3-8b-8192",
            temperature=temperature,
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")