from app.llm.client import llm
from app.graph.state import TravelState


def accommodation_agent(state: TravelState) -> dict:
    """
    Research accommodation options for the requested trip.

    This agent works with any destination, currency, budget,
    duration, and number of travelers.
    """

    destination = state.get("destination", "")
    duration_days = state.get("duration_days", 1)
    travelers = state.get("travelers", 1)
    budget = state.get("budget", 0)
    currency = state.get("currency", "UNKNOWN")

    preferences = state.get("preferences", [])
    constraints = state.get("constraints", [])

    # Normal trip calculation:
    # 5 days = 4 nights
    nights = max(duration_days - 1, 1)

    # Accommodation should not consume the entire trip budget.
    accommodation_budget = float(budget) * 0.45

    prompt = f"""
You are the Accommodation Agent in an Agentic AI Travel
Planning System.

Research practical accommodation options for the exact trip
provided below.

TRIP DETAILS
============

Destination: {destination}
Duration: {duration_days} days
Number of Travelers: {travelers}
Number of Nights: {nights}
Total Trip Budget: {budget} {currency}

Preferences:
{preferences}

Constraints:
{constraints}

IMPORTANT DESTINATION RULE
==========================

The destination is:

{destination}

You MUST provide accommodation information for {destination}.

Do NOT replace the destination with Dubai.

Do NOT replace the destination with Tokyo.

Do NOT assume any particular destination.

Use the destination supplied by the user.

IMPORTANT BUDGET RULE
=====================

The total trip budget is:

{budget} {currency}

Accommodation is only one part of the trip.

The traveler may also need money for:

- Food
- Transportation
- Attractions
- Activities
- Miscellaneous expenses

As a planning guideline, try to keep accommodation around
or below approximately:

{accommodation_budget:.2f} {currency}

This is NOT a strict rule.

If accommodation is normally more expensive at the requested
destination, explain that clearly.

Do not claim live prices or live availability.

All prices must be approximate.

ACCOMMODATION OPTIONS
=====================

Provide 3 practical accommodation options or categories
appropriate for the destination.

Examples may include:

- Budget hotel
- Mid-range hotel
- Hostel
- Guesthouse
- Apartment
- Homestay
- Resort

Choose appropriate options for the requested destination.

For each option provide:

1. Name or accommodation type
2. Area/location
3. Approximate price per night
4. Approximate total price for the stay
5. Currency
6. Why it is suitable
7. Important limitation

PRICE CALCULATION
=================

Number of nights: {nights}

Approximate total accommodation cost should be based on:

nightly price × {nights} nights

Do not incorrectly multiply the stay price by the number
of travelers unless the price is explicitly per person.

FINAL RECOMMENDATION
====================

Give one practical recommendation based on:

- Total trip budget
- Number of travelers
- Duration
- Destination
- Preferences
- Constraints

Do not automatically select the most expensive option.

OUTPUT FORMAT
=============

DESTINATION:
{destination}

OPTION_1:
NAME:
AREA:
PRICE_PER_NIGHT:
TOTAL_STAY_PRICE:
CURRENCY:
SUITABILITY:
LIMITATION:

OPTION_2:
NAME:
AREA:
PRICE_PER_NIGHT:
TOTAL_STAY_PRICE:
CURRENCY:
SUITABILITY:
LIMITATION:

OPTION_3:
NAME:
AREA:
PRICE_PER_NIGHT:
TOTAL_STAY_PRICE:
CURRENCY:
SUITABILITY:
LIMITATION:

RECOMMENDED_OPTION:

RECOMMENDATION_REASON:

RECOMMENDED_TOTAL_COST:

CURRENCY:
{currency}

IMPORTANT_NOTE:
Prices and availability are approximate and may vary.

Remember:

The destination is {destination}.

Never substitute another destination.
"""

    print("\n===== ACCOMMODATION AGENT =====")
    print("Researching accommodation options...")

    response = llm.invoke(prompt)

    research = response.content.strip()

    print("Accommodation research completed.")

    return {
        "accommodation_options": [
            {
                "research": research
            }
        ]
    }