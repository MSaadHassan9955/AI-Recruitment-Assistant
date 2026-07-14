"""
Chain 1: Resume Analysis

prompt | llm | StrOutputParser() -- same pattern taught in class.
Produces summary, match score, skills, and HR recommendation.
"""

from langchain_core.output_parsers import StrOutputParser

from ai.llm import llm
from ai.prompts.analysis_prompt import analysis_prompt

analysis_chain = analysis_prompt | llm | StrOutputParser()
