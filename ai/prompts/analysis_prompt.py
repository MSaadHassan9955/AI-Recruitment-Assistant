"""
Prompt for Chain 1: Resume Analysis

Covers Modules 4, 5, 6, 7 combined into one structured JSON output
(Module 9). Kept in its own file, separate from Chain 2's prompt,
as instructed by sir.
"""

from langchain_core.prompts import ChatPromptTemplate

analysis_prompt = ChatPromptTemplate.from_template(
    """
You are an HR recruitment assistant. Compare the candidate's resume
against the job description and analyze it carefully.

Job Description:
{jd_text}

Resume:
{resume_text}

Return ONLY a valid JSON object, with no extra text and no markdown
formatting, using exactly this schema:

{{
  "candidate_name": "candidate's full name extracted from the resume",
  "summary": "2-3 sentence summary of education, experience and key skills",
  "match_score": integer from 0 to 100,
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "extra_skills": ["skill1", "skill2"],
  "recommendation": "Hire" or "Interview" or "Reject",
  "justification": "short reason for the recommendation"
}}

Follow this exact rule to decide "recommendation" based on match_score,
do not use your own judgment instead of this rule:
- match_score 80 or above -> "Hire"
- match_score 60 to 79 -> "Interview"
- match_score below 60 -> "Reject"
"""
)
