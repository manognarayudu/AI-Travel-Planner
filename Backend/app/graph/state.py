from typing import Any, TypedDict


class TravelState(TypedDict, total=False):
    # ========================================================
    # USER REQUEST
    # ========================================================

    user_query: str

    # ========================================================
    # TRAVEL REQUIREMENTS
    # ========================================================

    destination: str
    duration_days: int
    travelers: int

    budget: float
    currency: str

    preferences: list[Any]
    constraints: list[Any]

    # ========================================================
    # DESTINATION RESEARCH
    # ========================================================

    destination_info: dict[str, Any]

    # ========================================================
    # ACCOMMODATION
    # ========================================================

    accommodation_options: list[Any]
    accommodation_cost: float

    # ========================================================
    # TRANSPORT
    # ========================================================

    transport_options: list[Any]
    transport_cost: float

    # ========================================================
    # WEATHER
    # ========================================================

    weather: dict[str, Any]

    # ========================================================
    # BUDGET
    # ========================================================

    food_cost: float
    activities_cost: float
    miscellaneous_cost: float

    estimated_cost: float
    budget_remaining: float
    budget_status: str

    warnings: list[str]

    # ========================================================
    # ITINERARY
    # ========================================================

    itinerary: list[Any]

    # ========================================================
    # OPTIMIZATION
    # ========================================================

    optimized_itinerary: str
    optimization_status: str