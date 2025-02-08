# llm_agent.py
import openai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_vacation_recommendation(holiday_dates, extra_days=2):
    """
    Sends a prompt to the OpenAI API to determine the best extended vacation periods.
    :param holiday_dates: List of holiday dates (datetime.date)
    :param extra_days: Number of extra leave days the user can take
    :return: The recommendation as a string.
    """
    # Convert dates to strings and sort them
    dates_str = "\n".join(str(date) for date in sorted(holiday_dates))
    prompt = f"""I have the following holiday dates in my calendar:
{dates_str}

I am looking to maximize my vacation by taking {extra_days} extra days off.
Please suggest the best period(s) for an extended vacation by combining weekends and these holidays.
List the optimal vacation period(s) along with the dates I would need to take off.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use "gpt-4" if available
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        suggestion = response['choices'][0]['message']['content']
    except Exception as e:
        suggestion = f"Error calling OpenAI API: {e}"
    return suggestion
