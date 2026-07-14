"""
Output Parsing

The AI is asked to return JSON, but it sometimes wraps it in markdown
(```json ... ```) or adds extra text around it. This function cleans
that up and safely converts it into a Python dictionary.
"""

import json
import re


def parse_json_output(raw_output, fallback):
    """
    Converts the AI's raw text response into a Python dictionary.

    fallback: what to return if the response can't be parsed as JSON,
    so the app never crashes even if the AI gives a bad response.
    """
    # remove markdown code fences if present
    cleaned = re.sub(r"```json|```", "", raw_output).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # try to find the first { ... } block in the text
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        return fallback
