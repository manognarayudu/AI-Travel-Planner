from app.graph.graph import travel_graph


initial_state = {
    "user_query": "Plan a 5-day Dubai trip for two people with a budget of AED 8000",
    "destination": None,
    "duration_days": None,
    "travelers": None,
    "budget": None,
    "currency": None,
    "preferences": [],
    "constraints": [],
}


print("===== INPUT STATE =====")
print(initial_state)

print("\n===== RUNNING LANGGRAPH =====")

final_state = travel_graph.invoke(initial_state)

print("\n===== FINAL STATE =====")
print(final_state)