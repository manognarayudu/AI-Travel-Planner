from app.agents.destination_agent import research_destination


print("===== DESTINATION AGENT TEST =====")

result = research_destination(
    destination="Dubai",
    duration_days=5
)

print("\n===== DESTINATION RESEARCH =====")
print(result["research"])