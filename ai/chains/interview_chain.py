"""
Chain 2: Interview Questions

prompt | llm | StrOutputParser() -- same pattern as Chain 1, but this
chain is only invoked when match_score >= 80 (see ai/pipeline.py).
"""

from langchain_core.output_parsers import StrOutputParser

from ai.llm import llm
from ai.prompts.interview_prompt import interview_prompt

interview_chain = interview_prompt | llm | StrOutputParser()
