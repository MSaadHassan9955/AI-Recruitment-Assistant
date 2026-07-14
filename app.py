"""
AI Recruitment Assistant Dashboard - Main App

This file only handles the UI (Module 1). All the real work
(PDF reading, cleaning, AI analysis) happens in utils/ and ai/.
"""

import streamlit as st
import pandas as pd

from utils.pdf_reader import read_and_clean_pdf
from ai.pipeline import analyze_resume

st.set_page_config(page_title="AI Recruitment Assistant", layout="wide")

st.title("AI Recruitment Assistant Dashboard")
st.caption("Upload a job description and one or more resumes to get AI-powered candidate analysis.")


# ---------------------------------------------------------
# Sidebar: uploads
# ---------------------------------------------------------
st.sidebar.header("Upload Files")

jd_file = st.sidebar.file_uploader("Upload Job Description (PDF)", type=["pdf"])

resume_files = st.sidebar.file_uploader(
    "Upload Resume(s)",
    type=["pdf"],
    accept_multiple_files=True,
)

analyze_clicked = st.sidebar.button("Analyze Resume(s)")


# ---------------------------------------------------------
# Main logic
# ---------------------------------------------------------
if analyze_clicked:

    if not jd_file:
        st.warning("Please upload a job description first.")
    elif not resume_files:
        st.warning("Please upload at least one resume.")
    else:
        jd_text = read_and_clean_pdf(jd_file)

        # Module 2: extract + display text (useful to show working in the demo)
        with st.expander("View Extracted Job Description Text"):
            st.text(jd_text)

        results = []
        with st.spinner("Analyzing resume(s)... this may take a moment"):
            for resume_file in resume_files:
                resume_text = read_and_clean_pdf(resume_file)

                with st.expander(f"View Extracted Text - {resume_file.name}"):
                    st.text(resume_text)

                result = analyze_resume(resume_text, jd_text)
                results.append(result)

        # ---------------------------------------------------
        # Case 1: single resume -> show a detailed result card
        # ---------------------------------------------------
        if len(results) == 1:
            r = results[0]
            st.subheader(r.get("candidate_name", "Candidate"))
            st.metric("Match Score", f"{r.get('match_score', 0)}%")
            st.write("**Summary:**", r.get("summary", ""))

            # Module: "skills identified in the CV" -- matching + extra skills
            # found in the resume (as opposed to missing skills, shown separately)
            identified_skills = r.get("matching_skills", []) + r.get("extra_skills", [])
            st.write("**Skills Identified:**", ", ".join(identified_skills) or "None")
            st.write("**Missing Skills:**", ", ".join(r.get("missing_skills", [])) or "None")
            st.write("**Recommendation:**", r.get("recommendation", ""))
            st.write("**Justification:**", r.get("justification", ""))

            if r.get("interview_questions"):
                st.write("**Interview Questions (Technical):**")
                for q in r["interview_questions"].get("technical", []):
                    st.write("-", q)
                st.write("**Interview Questions (HR):**")
                for q in r["interview_questions"].get("hr", []):
                    st.write("-", q)

        # ---------------------------------------------------
        # Case 2: multiple resumes -> comparison table
        # ---------------------------------------------------
        else:
            table_rows = []
            for r in results:
                table_rows.append({
                    "Candidate Name": r.get("candidate_name", "Unknown"),
                    "Matching Score": r.get("match_score", 0),
                    "AI Short Description": r.get("summary", ""),
                    "Missing Skills": ", ".join(r.get("missing_skills", [])),
                    "Recommendation": r.get("recommendation", ""),
                })

            df = pd.DataFrame(table_rows)
            df = df.sort_values("Matching Score", ascending=False)

            st.subheader("Candidate Comparison")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Export as CSV",
                data=csv,
                file_name="candidate_comparison.csv",
                mime="text/csv",
            )

            # Show interview questions for shortlisted candidates below the table
            for r in results:
                if r.get("interview_questions"):
                    with st.expander(f"Interview Questions - {r.get('candidate_name')}"):
                        st.write("**Technical:**")
                        for q in r["interview_questions"].get("technical", []):
                            st.write("-", q)
                        st.write("**HR:**")
                        for q in r["interview_questions"].get("hr", []):
                            st.write("-", q)
