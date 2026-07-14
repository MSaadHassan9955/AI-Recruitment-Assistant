Created by : "Muhammad Saad Hassan"

Deployed App Link : https://ai-recruitment-assistant-hedyheggtedh9ap7ow6esc.streamlit.app/


# AI Recruitment Assistant Dashboard

A Streamlit app that helps HR screen resumes automatically. Upload a
job description and one or more resumes, and the app uses Gemini
(through LangChain) to generate a summary, match score, missing
skills, and hiring recommendation for each candidate. If a candidate
scores 80% or above, the app also generates interview questions.

## How it works

```
Upload Resume(s) + JD
        |
PDF Text Extraction (utils/pdf_reader.py)
        |
Text Cleaning (utils/pdf_reader.py)
        |
LangChain Analysis Chain (ai/chains.py)
   -> Summary, Match Score, Missing Skills, Recommendation
        |
Score >= 80%? --> Interview Questions Chain (ai/chains.py)
        |
Single resume  -> detailed result card
2+ resumes     -> comparison table + CSV export
```

## Project Structure

```
AI-Recruitment-Assistant/
├── app.py                        # Streamlit UI only, no logic
├── requirements.txt
├── .env.example
│
├── utils/
│   ├── pdf_reader.py              # extract + clean PDF text
│   └── parser.py                  # safely parse LLM JSON output
│
├── ai/
│   ├── llm.py                     # Gemini model setup
│   ├── pipeline.py                # combines the two chains + conditional logic
│   ├── prompts/
│   │   ├── analysis_prompt.py      # prompt for Chain 1
│   │   └── interview_prompt.py     # prompt for Chain 2
│   └── chains/
│       ├── analysis_chain.py       # Chain 1: summary, score, skills, recommendation
│       └── interview_chain.py      # Chain 2: interview questions (conditional)
│
├── data/                          # sample resumes + job descriptions
└── outputs/                       # exported CSVs
```

Each chain has its own file, and each chain's prompt is stored in its
own file too — this was an explicit requirement from sir (no shared
`chains.py` or `prompts.py` holding multiple chains/prompts together).

## Setup

1. Clone the repo and move into the folder:
   ```
   git clone <your-repo-url>
   cd AI-Recruitment-Assistant
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Add your Gemini API key. Copy `.env.example` to `.env` and fill it in:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. Run the app:
   ```
   streamlit run app.py
   ```

## Usage

1. Upload a job description PDF in the sidebar.
2. Upload one or more resume PDFs.
3. Click "Analyze Resume(s)".
4. For a single resume, view the detailed result card.
5. For multiple resumes, view the ranked comparison table and export it as CSV.

## Notes

- Only candidates scoring 80% or above get AI-generated interview questions.
- The comparison table columns match the required format: Candidate Name,
  Matching Score, AI Short Description, Missing Skills, Recommendation.
