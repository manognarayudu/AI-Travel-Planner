from app.llm.client import llm
from app.graph.state import TravelState


def itinerary_agent(state: TravelState) -> dict:
    """
    Generates a practical day-by-day itinerary using the information
    collected by the previous agents.
    """

    destination = state.get("destination", "")
    duration_days = state.get("duration_days") or 1
    travelers = state.get("travelers") or 1
    budget = state.get("budget") or 0
    currency = state.get("currency") or "UNKNOWN"

    preferences = state.get("preferences", [])
    constraints = state.get("constraints", [])

    destination_info = state.get("destination_info", {})
    accommodation = state.get("accommodation_options", [])
    transport = state.get("transport_options", [])
    weather = state.get("weather", {})

    accommodation_cost = state.get("accommodation_cost") or 0
    transport_cost = state.get("transport_cost") or 0
    food_cost = state.get("food_cost") or 0
    activities_cost = state.get("activities_cost") or 0
    miscellaneous_cost = state.get("miscellaneous_cost") or 0

    estimated_cost = state.get("estimated_cost") or 0
    budget_remaining = state.get("budget_remaining") or 0
    budget_status = state.get("budget_status", "UNKNOWN")

    prompt = f"""
You are the Itinerary Agent in an Agentic AI Travel Planning System.

Create a practical day-by-day itinerary for the user's EXACT trip.

==================================================
TRIP REQUIREMENTS
==================================================

Destination:
{destination}

Duration:
{duration_days} days

Travelers:
{travelers}

Budget:
{budget} {currency}

Preferences:
{preferences}

Constraints:
{constraints}

==================================================
DESTINATION INFORMATION
==================================================

{destination_info}

==================================================
ACCOMMODATION
==================================================

{accommodation}

Approximate accommodation cost:
{accommodation_cost} {currency}

==================================================
TRANSPORT
==================================================

{transport}

Approximate transport cost:
{transport_cost} {currency}

==================================================
WEATHER
==================================================

{weather}

==================================================
BUDGET
==================================================

Accommodation:
{accommodation_cost} {currency}

Transport:
{transport_cost} {currency}

Food:
{food_cost} {currency}

Activities:
{activities_cost} {currency}

Miscellaneous:
{miscellaneous_cost} {currency}

Total estimated cost:
{estimated_cost} {currency}

Remaining budget:
{budget_remaining} {currency}

Budget status:
{budget_status}

==================================================
IMPORTANT RULES
==================================================

1. Create EXACTLY {duration_days} days.

2. The destination is EXACTLY {destination}.

3. Never replace the destination with another city or country.

4. Never assume the destination is Dubai.

5. Never assume the destination is Tokyo.

6. All attractions and activities must be relevant to {destination}.

7. Do not invent attractions that do not exist.

8. Use the destination research provided above.

9. Consider geographical proximity when grouping activities.

10. Avoid unnecessarily long travel between activities.

11. Consider available transportation.

12. Consider the accommodation location when possible.

13. Consider the weather information.

14. Respect the user's preferences.

15. Respect the user's constraints.

16. Keep the plan consistent with the estimated budget.

17. Do not claim live prices.

18. Do not claim live opening hours.

19. Do not claim live availability.

20. Use approximate costs only.

21. Do not create an unrealistic number of activities in one day.

22. Include reasonable rest/free time.

23. If information is uncertain, explicitly say it is approximate.

==================================================
FORMAT
==================================================

DAY 1

Morning:
Activity:
Location:
Estimated Cost:
Notes:

Afternoon:
Activity:
Location:
Estimated Cost:
Notes:

Evening:
Activity:
Location:
Estimated Cost:
Notes:

Day Summary:


DAY 2

Morning:
Activity:
Location:
Estimated Cost:
Notes:

Afternoon:
Activity:
Location:
Estimated Cost:
Notes:

Evening:
Activity:
Location:
Estimated Cost:
Notes:

Day Summary:


Continue exactly the same structure until DAY {duration_days}.

==================================================
FINAL SUMMARY
==================================================

TRIP ITINERARY SUMMARY:

Destination:
{destination}

Total Days:
{duration_days}

Travelers:
{travelers}

Estimated Trip Cost:
{estimated_cost} {currency}

Budget Remaining:
{budget_remaining} {currency}

Budget Status:
{budget_status}

IMPORTANT WARNINGS:
Mention important approximate-price, weather, transportation,
or planning limitations.

Return ONLY the itinerary.
"""

    print("\n===== ITINERARY AGENT =====")
    print("Creating day-by-day itinerary...")

    response = llm.invoke(prompt)

    itinerary_text = response.content.strip()

    print("Itinerary generation completed.")

    return {
        "itinerary": [
            {
                "plan": itinerary_text
            }
        ]
    }