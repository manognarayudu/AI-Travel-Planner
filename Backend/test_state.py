from app.graph.state import TravelState


state: TravelState = {
    "user_query": "Plan a 5-day Dubai trip",
    "destination": "Dubai",
    "duration_days": 5,
    "travelers": 2,
    "budget": 8000,
    "currency": "AED",
    "preferences": ["major attractions"],
    "constraints": []
}


print("===== TRAVEL STATE =====")

for key, value in state.items():
    print(f"{key}: {value}")