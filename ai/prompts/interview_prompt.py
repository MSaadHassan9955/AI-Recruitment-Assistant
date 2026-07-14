"""
Prompt for Chain 2: Interview Questions

Covers Module 8. Kept separate from the analysis prompt because this
chain only runs conditionally (match_score >= 80), as instructed by
sir in the voice note.
"""

from langchain_core.prompts import ChatPromptTemplate

interview_prompt = ChatPromptTemplate.from_template(
    """
You are an HR recruitment assistant. Based on the resume and job
description below, generate interview questions for this candidate.

Job Description:
{jd_text}

Resume:
{resume_text}

Return ONLY a valid JSON object with exactly this schema:

{{
  "technical": ["question1", "question2", "question3"],
  "hr": ["question1", "question2", "question3"]
}}
"""
)
