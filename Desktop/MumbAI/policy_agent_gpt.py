import openai
import json
from dotenv import load_dotenv
import os

# Initialize the OpenAI client
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.Client(api_key=api_key)


def get_daily_policy(daily_data):
    system_prompt = """
You are the Chief Risk Officer of Riverline Bank. Generate today's underwriting policy.
Balance portfolio growth with NPA risk. Use inputs like interest rate, NPA, income, personality risk.

Return a JSON with:
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

    response = client.responses.create(
        model="gpt-4.1",
        input=f"{system_prompt}\n{user_prompt}"
    )

    # Print the response for debugging
    print("API Response:", response.output_text)

    try:
        return json.loads(response.output_text)
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e)
        return None