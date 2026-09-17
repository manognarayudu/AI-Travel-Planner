from app.agents.requirement_agent import extract_requirements
from app.schemas.travel import TravelRequest


print("Starting Requirement Agent test...")


request = TravelRequest(
    query=(
        "Plan a 5-day Dubai trip for two people "
        "with a total budget of AED 8,000. "
        "Include accommodation, major attractions, "
        "and local transportation."
    )
)


print("Sending request to Gemini...")


requirements = extract_requirements(request)


print("\n===== EXTRACTED REQUIREMENTS =====")
print(requirements)

print("\n===== AS DICTIONARY =====")
print(requirements.model_dump())