"""
Pipeline

This file connects the two chains together, so app.py doesn't need
to know how they work internally.

Step 1: Ask the AI to analyze the resume (summary, score, skills).
Step 2: Decide Hire / Interview / Reject ourselves, based on the score.
Step 3: If the score is 80 or above, ask the AI for interview questions too.
"""

from ai.chains.analysis_chain import analysis_chain
from ai.chains.interview_chain import interview_chain
from utils.parser import parse_json_output

ANALYSIS_FALLBACK = {
    "candidate_name": "Unknown",
    "summary": "Could not parse AI response.",
    "match_score": 0,
    "matching_skills": [],
    "missing_skills": [],
    "extra_skills": [],
    "recommendation": "Reject",
    "justification": "AI response could not be parsed.",
}

INTERVIEW_FALLBACK = {
    "technical": [],
    "hr": [],
}


def analyze_resume(resume_text, jd_text):
    """
    Runs the full pipeline for one resume and returns everything as
    a single dictionary, ready to be shown in the UI.
    """
    # Step 1: ask the AI to analyze the resume against the job description
    analysis_raw = analysis_chain.invoke({
        "resume_text": resume_text,
        "jd_text": jd_text,
    })
    result = parse_json_output(analysis_raw, fallback=ANALYSIS_FALLBACK)

    # if the AI's answer didn't make sense, just ask it again once
    if result.get("candidate_name") == "Unknown":
        analysis_raw = analysis_chain.invoke({
            "resume_text": resume_text,
            "jd_text": jd_text,
        })
        result = parse_json_output(analysis_raw, fallback=ANALYSIS_FALLBACK)

    score = result.get("match_score", 0)

    # Step 2: decide the recommendation ourselves, based on the score,
    # so it's always consistent (Hire / Interview / Reject)
    if score >= 80:
        result["recommendation"] = "Hire"
    elif score >= 60:
        result["recommendation"] = "Interview"
    else:
        result["recommendation"] = "Reject"

    # Step 3: only ask for interview questions if the score is 80 or above
    if score >= 80:
        interview_raw = interview_chain.invoke({
            "resume_text": resume_text,
            "jd_text": jd_text,
        })
        questions = parse_json_output(interview_raw, fallback=INTERVIEW_FALLBACK)

        # if the AI's answer didn't make sense, just ask it again once
        if not questions.get("technical") and not questions.get("hr"):
            interview_raw = interview_chain.invoke({
                "resume_text": resume_text,
                "jd_text": jd_text,
            })
            questions = parse_json_output(interview_raw, fallback=INTERVIEW_FALLBACK)

        result["interview_questions"] = questions
    else:
        result["interview_questions"] = None

    return result
