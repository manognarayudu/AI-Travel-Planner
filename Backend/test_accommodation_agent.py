from app.agents.accommodation_agent import accommodation_agent


state = {
    "user_query": "Plan a 5-day Dubai trip for two people with a budget of AED 8000",

    "destination": "Dubai",
    "duration_days": 5,
    "travelers": 2,
    "budget": 8000,
    "currency": "AED",

    "preferences": ["major attractions"],
    "constraints": []
}


print("===== ACCOMMODATION AGENT TEST =====")

result = accommodation_agent(state)

print("\n===== RESULT =====")
print(result)
