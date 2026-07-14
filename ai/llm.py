"""
LLM Setup

This file sets up the LLM through LangChain using OpenRouter --
the same connection method taught in class (ChatOpenAI pointed at
OpenRouter's base_url). Switched from direct Gemini API because
Gemini's free tier wasn't provisioned for this account/region.
Sir approved OpenRouter (and Grok) as alternatives.

Using OpenRouter's "meta-llama/llama-3.3-70b-instruct:free" model -- a
specific, stable free model (rather than the auto-router) so that
match scores stay consistent between runs of the same resume.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    model="openai/gpt-oss-20b:free",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.1,
)

