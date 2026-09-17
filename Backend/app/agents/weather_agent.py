from app.llm.client import llm
from app.graph.state import TravelState


def weather_agent(state: TravelState) -> dict:
    """
    Generates destination-specific typical/seasonal weather information.

    It does not claim to provide live weather forecasts.
    """

    destination = state.get("destination", "")
    duration_days = state.get("duration_days")

    if not destination:
        return {
            "weather": {
                "research": "Weather information unavailable because the destination was not provided."
            }
        }

    prompt = f"""
You are the Weather Agent in an AI Travel Planning System.

DESTINATION:
{destination}

TRIP DURATION:
{duration_days if duration_days else "Not specified"} days

Your task is to provide useful typical/seasonal weather information
for EXACTLY this destination:

{destination}

IMPORTANT:

- The destination is {destination}.
- Do not replace it with another destination.
- Do not mention unrelated cities.
- Do not use Tokyo unless Tokyo is the actual destination.
- Do not use Dubai unless Dubai is the actual destination.
- Do not claim live weather data.
- Do not provide a fake future forecast.
- If travel dates are unavailable, provide general typical/seasonal
  conditions.
- Clearly state that the information is approximate.

Provide:

DESTINATION:
{destination}

WEATHER TYPE:
Typical / Seasonal

TEMPERATURE:
Typical approximate range

RAINFALL:
Typical rainfall or weather conditions

CLOTHING:
Recommended clothing

OUTDOOR ACTIVITIES:
How weather may affect outdoor activities

PRECAUTIONS:
Useful weather precautions

WEATHER SUMMARY:
Short practical summary for someone visiting {destination}.

Return only the requested information.
"""

    print("\n===== WEATHER AGENT =====")
    print("Researching weather information...")

    response = llm.invoke(prompt)

    research = response.content.strip()

    print("Weather research completed.")

    return {
        "weather": {
            "research": research
        }
    }