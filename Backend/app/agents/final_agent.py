from app.graph.state import TravelState


def final_agent(state: TravelState) -> dict:
    """
    Prepares the final consolidated travel plan.

    The final agent does not recalculate or modify any costs.
    It simply collects the results produced by the previous agents.
    """

    optimized_itinerary = state.get(
        "optimized_itinerary",
        ""
    )

    itinerary = state.get(
        "itinerary",
        []
    )

    # Prefer the optimized itinerary when available.
    if optimized_itinerary:
        final_itinerary = optimized_itinerary
    else:
        final_itinerary = itinerary

    return {
        "final_plan": {
            "destination": state.get("destination", ""),
            "duration_days": state.get("duration_days", 0),
            "travelers": state.get("travelers", 1),
            "budget": state.get("budget", 0),
            "currency": state.get("currency", ""),

            "destination_info": state.get(
                "destination_info",
                {}
            ),

            "accommodation": state.get(
                "accommodation_options",
                []
            ),

            "transport": state.get(
                "transport_options",
                []
            ),

            "weather": state.get(
                "weather",
                {}
            ),

            "budget_breakdown": {
                "accommodation_cost": state.get(
                    "accommodation_cost",
                    0
                ),
                "transport_cost": state.get(
                    "transport_cost",
                    0
                ),
                "food_cost": state.get(
                    "food_cost",
                    0
                ),
                "activities_cost": state.get(
                    "activities_cost",
                    0
                ),
                "miscellaneous_cost": state.get(
                    "miscellaneous_cost",
                    0
                ),
                "total_estimated_cost": state.get(
                    "estimated_cost",
                    0
                ),
                "budget_remaining": state.get(
                    "budget_remaining",
                    0
                ),
                "budget_status": state.get(
                    "budget_status",
                    "UNKNOWN"
                ),
            },

            "itinerary": final_itinerary,

            "optimization": {
                "status": state.get(
                    "optimization_status",
                    "UNKNOWN"
                ),
                "optimized_itinerary": optimized_itinerary,
            },

            "warnings": state.get(
                "warnings",
                []
            ),
        }
    }