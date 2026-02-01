"""Configuration for the Gradio AI chat application."""

DEFAULT_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
FALLBACK_MODEL = "meta-llama/Llama-3.2-3B-Instruct"

MAX_NEW_TOKENS = 512
TEMPERATURE = 0.7
TOP_P = 0.9
REPETITION_PENALTY = 1.05

SYSTEM_PROMPT = (
    "You are a helpful, concise assistant. Answer clearly and politely."
)
