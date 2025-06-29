import openai
import json
from dotenv import load_dotenv
import os
import re
# import streamlit as st  # No longer needed

# Initialize the OpenAI client
load_dotenv()
# Only use .env/environment variable for API key
api_key = os.getenv("OPENAI_API_KEY")
client = openai.Client(api_key=api_key)


def get_daily_policy(daily_data):
    system_prompt = """
You are the Chief Risk Officer of Riverline Bank. Generate today's underwriting policy.
Balance portfolio growth with NPA risk. Use inputs like interest rate, NPA, income, personality risk.

Return ONLY valid JSON with:
- min_credit_score
- min_income
- deny_if_personality
- reason
"""

    user_prompt = f"""
Bank Data:
Interest Rate: {daily_data['interest_rate']}%
NPA Rate: {daily_data['npa_rate']}%
Avg Income: {daily_data['avg_income']}
Personality Risk: {daily_data['personality_risk']}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=f"{system_prompt}\n{user_prompt}"
        )
    except Exception as api_error:
        print("OpenAI API Error:", api_error)
        return None

    # Print the response for debugging
    print("API Response:", getattr(response, 'output_text', str(response)))
    output = getattr(response, 'output_text', str(response)).strip()
    # Remove markdown code block if present
    if output.startswith("```json"):
        output = re.sub(r"^```json\\s*|\\s*```$", "", output, flags=re.DOTALL)
    elif output.startswith("```"):
        output = re.sub(r"^```\\s*|\\s*```$", "", output, flags=re.DOTALL)
    try:
        return json.loads(output)
    except json.JSONDecodeError as e:
        print("JSONDecodeError: Could not parse policy JSON.")
        print("Raw output was:", output)
        print("Error details:", e)
        return None