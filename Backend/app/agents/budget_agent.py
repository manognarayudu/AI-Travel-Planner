from app.llm.client import llm
from app.graph.state import TravelState


def _extract_number(text: str, keyword: str) -> float:
    """
    Extract the first numeric value appearing after a keyword.

    Example:
    ACCOMMODATION_COST: 2500
    """

    import re

    pattern = rf"{keyword}\s*:\s*([0-9]+(?:\.[0-9]+)?)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return float(match.group(1))

    return 0.0


def budget_agent(state: TravelState) -> dict:
    """
    Calculates the approximate travel budget.

    The calculation is performed locally using the costs
    estimated by the LLM.

    This prevents the LLM from performing inconsistent
    arithmetic.
    """

    destination = state.get("destination", "")
    duration_days = state.get("duration_days", 1)
    travelers = state.get("travelers", 1)

    budget = float(
        state.get("budget", 0) or 0
    )

    currency = state.get(
        "currency",
        "UNKNOWN"
    )

    accommodation = state.get(
        "accommodation_options",
        []
    )

    transport = state.get(
        "transport_options",
        []
    )

    preferences = state.get(
        "preferences",
        []
    )

    constraints = state.get(
        "constraints",
        []
    )

    accommodation_text = str(
        accommodation
    )

    transport_text = str(
        transport
    )

    prompt = f"""
You are the Budget Agent in an Agentic AI Travel Planning System.

Estimate realistic approximate travel expenses.

TRIP DETAILS
============

Destination:
{destination}

Duration:
{duration_days} days

Travelers:
{travelers}

Total Available Budget:
{budget} {currency}

Preferences:
{preferences}

Constraints:
{constraints}

ACCOMMODATION RESEARCH
======================

{accommodation_text}

TRANSPORT RESEARCH
==================

{transport_text}

IMPORTANT RULES
===============

1. The destination is {destination}.

2. Do not replace the destination with another destination.

3. Use the requested currency: {currency}.

4. Accommodation, transport, food, activities and
   miscellaneous expenses are separate categories.

5. Provide approximate estimates only.

6. Do not claim live prices.

7. Do not add the same expense twice.

8. Food should represent the complete trip, not a
   per-meal amount.

9. Activity cost should represent the complete trip.

10. Miscellaneous cost should represent the complete trip.

11. Keep estimates realistic for {travelers} travelers.

12. Do not include international flight costs unless
    the user explicitly requested flights.

RETURN EXACTLY THIS FORMAT:

ACCOMMODATION_COST: <number>

TRANSPORT_COST: <number>

FOOD_COST: <number>

ACTIVITIES_COST: <number>

MISCELLANEOUS_COST: <number>

Do NOT calculate TOTAL_COST.

Do NOT calculate BUDGET_REMAINING.

Do NOT calculate BUDGET_STATUS.

Only provide the five expense categories above.

Use {currency} for all values.
"""

    print("\n===== BUDGET AGENT =====")
    print("Estimating trip expenses...")

    response = llm.invoke(prompt)

    research = response.content.strip()

    # ========================================================
    # EXTRACT THE FIVE COST CATEGORIES
    # ========================================================

    accommodation_cost = _extract_number(
        research,
        "ACCOMMODATION_COST"
    )

    transport_cost = _extract_number(
        research,
        "TRANSPORT_COST"
    )

    food_cost = _extract_number(
        research,
        "FOOD_COST"
    )

    activities_cost = _extract_number(
        research,
        "ACTIVITIES_COST"
    )

    miscellaneous_cost = _extract_number(
        research,
        "MISCELLANEOUS_COST"
    )

    # ========================================================
    # CALCULATE TOTAL LOCALLY
    # ========================================================

    estimated_cost = (
        accommodation_cost
        + transport_cost
        + food_cost
        + activities_cost
        + miscellaneous_cost
    )

    budget_remaining = (
        budget - estimated_cost
    )

    if estimated_cost <= budget:
        budget_status = "WITHIN_BUDGET"
    else:
        budget_status = "OVER_BUDGET"

    # ========================================================
    # CREATE SUMMARY
    # ========================================================

    summary = (
        f"Approximate trip cost for "
        f"{duration_days} days in {destination} "
        f"for {travelers} travelers is "
        f"{estimated_cost:.2f} {currency}. "
        f"Remaining budget is "
        f"{budget_remaining:.2f} {currency}."
    )

    print("Budget calculation completed.")

    print(
        f"ACCOMMODATION_COST: "
        f"{accommodation_cost:.2f}"
    )

    print(
        f"TRANSPORT_COST: "
        f"{transport_cost:.2f}"
    )

    print(
        f"FOOD_COST: "
        f"{food_cost:.2f}"
    )

    print(
        f"ACTIVITIES_COST: "
        f"{activities_cost:.2f}"
    )

    print(
        f"MISCELLANEOUS_COST: "
        f"{miscellaneous_cost:.2f}"
    )

    print(
        f"TOTAL_COST: "
        f"{estimated_cost:.2f}"
    )

    print(
        f"BUDGET_REMAINING: "
        f"{budget_remaining:.2f}"
    )

    print(
        f"BUDGET_STATUS: "
        f"{budget_status}"
    )

    print(
        f"SUMMARY: "
        f"{summary}"
    )

    return {
        "accommodation_cost": accommodation_cost,
        "transport_cost": transport_cost,
        "food_cost": food_cost,
        "activities_cost": activities_cost,
        "miscellaneous_cost": miscellaneous_cost,

        "estimated_cost": estimated_cost,

        "budget_remaining": budget_remaining,

        "budget_status": budget_status,

        "warnings": (
            []
            if budget_status == "WITHIN_BUDGET"
            else [
                "Estimated expenses exceed the available budget."
            ]
        ),
    }