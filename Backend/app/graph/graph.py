from langgraph.graph import StateGraph, START, END

from app.graph.state import TravelState
from app.agents.requirement_agent import extract_requirements
from app.agents.destination_agent import research_destination
from app.agents.accommodation_agent import accommodation_agent
from app.agents.transport_agent import transport_agent
from app.agents.weather_agent import weather_agent
from app.schemas.travel import TravelRequest
from app.agents.budget_agent import budget_agent
from app.agents.itinerary_agent import itinerary_agent
from app.agents.optimization_agent import optimization_agent
from app.agents.final_agent import final_agent
# ============================================================
# REQUIREMENT AGENT NODE
# ============================================================

def requirement_node(state: TravelState) -> dict:

    print("\n===== REQUIREMENT AGENT =====")
    print("Processing user request...")

    user_query = state.get("user_query", "").strip()

    request = TravelRequest(
        query=user_query
    )

    requirements = extract_requirements(request)

    print("Requirements extracted:")
    print(requirements)

    return {
        "destination": requirements.destination,
        "duration_days": requirements.duration_days,
        "travelers": requirements.travelers,
        "budget": requirements.budget,
        "currency": requirements.currency,
        "preferences": requirements.preferences,
        "constraints": requirements.constraints,
    }

# ============================================================
# DESTINATION AGENT NODE
# ============================================================

def destination_node(state: TravelState) -> dict:

    print("\n===== DESTINATION AGENT =====")
    print("Researching destination...")

    destination = state["destination"]

    destination_info = research_destination(destination)

    print("Destination research completed.")

    return {
        "destination_info": destination_info
    }


# ============================================================
# ACCOMMODATION AGENT NODE
# ============================================================

def accommodation_node(state: TravelState) -> dict:

    print("\n===== ACCOMMODATION AGENT =====")
    print("Searching for accommodation...")

    result = accommodation_agent(state)

    print("Accommodation search completed.")

    return result


# ============================================================
# TRANSPORT AGENT NODE
# ============================================================

def transport_node(state: TravelState) -> dict:

    print("\n===== TRANSPORT AGENT =====")
    print("Researching transport options...")

    result = transport_agent(state)

    print("Transport research completed.")

    return result


# ============================================================
# WEATHER AGENT NODE
# ============================================================

def weather_node(state: TravelState) -> dict:

    print("\n===== WEATHER AGENT =====")
    print("Checking weather information...")

    result = weather_agent(state)

    print("Weather research completed.")

    return result

# ============================================================
# OPTIMIZATION AGENT NODE
# ============================================================

def optimization_node(state: TravelState) -> dict:

    print("\n===== OPTIMIZATION AGENT =====")
    print("Checking itinerary feasibility...")

    result = optimization_agent(state)

    print("Optimization completed.")

    return result


# ============================================================
# CREATE LANGGRAPH
# ============================================================

builder = StateGraph(TravelState)


# ============================================================
# ADD NODES
# ============================================================

builder.add_node(
    "requirement_agent",
    requirement_node
)

builder.add_node(
    "destination_agent",
    destination_node
)

builder.add_node(
    "accommodation_agent",
    accommodation_node
)

builder.add_node(
    "transport_agent",
    transport_node
)

builder.add_node(
    "weather_agent",
    weather_node
)

builder.add_node(
    "budget_agent",
    budget_agent
)

builder.add_node(
    "itinerary_agent",
    itinerary_agent
)

builder.add_node(
    "optimization_agent",
    optimization_node
)

builder.add_node(
    "final_agent",
    final_agent
)

# ============================================================
# DEFINE GRAPH FLOW
# ============================================================

builder.add_edge(
    START,
    "requirement_agent"
)

builder.add_edge(
    "requirement_agent",
    "destination_agent"
)

builder.add_edge(
    "destination_agent",
    "accommodation_agent"
)

builder.add_edge(
    "accommodation_agent",
    "transport_agent"
)

builder.add_edge(
    "transport_agent",
    "weather_agent"
)

builder.add_edge(
    "weather_agent",
    "budget_agent"
)

builder.add_edge(
    "budget_agent",
    "itinerary_agent"
)

builder.add_edge(
    "itinerary_agent",
    "optimization_agent"
)

builder.add_edge(
    "optimization_agent",
    "final_agent"
)

builder.add_edge(
    "final_agent",
    END
)


# ============================================================
# COMPILE GRAPH
# ============================================================

travel_graph = builder.compile()