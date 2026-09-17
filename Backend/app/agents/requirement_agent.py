from app.llm.client import llm
from app.schemas.travel import TravelRequest, TravelRequirements


def extract_requirements(request: TravelRequest) -> TravelRequirements:
    """
    Extract travel requirements from the user's natural-language query.

    No destination, currency, budget, duration, or traveler count
    is hard-coded.
    """

    structured_llm = llm.with_structured_output(TravelRequirements)

    prompt = f"""
You are the Requirement Extraction Agent for a travel planning system.

Extract travel requirements from the user's request.

USER REQUEST:
{request.query}

Extract these fields:

1. destination
2. duration_days
3. travelers
4. budget
5. currency
6. preferences
7. constraints

RULES:

- Extract information from the user's request only.
- Never assume Dubai.
- Never assume Tokyo.
- Never assume any other destination.
- Never invent a budget.
- Never invent a currency.
- Never invent the number of travelers.
- Never invent the trip duration.
- Never invent preferences or constraints.
- Do not convert currencies.

DESTINATION:

Examples:

"5 days in Paris"
→ destination = Paris

"trip to Singapore"
→ destination = Singapore

"visit London for one week"
→ destination = London

"3 days in Goa"
→ destination = Goa

DURATION:

Convert:

"a week" → 7
"one week" → 7
"two weeks" → 14

Otherwise use the number explicitly provided.

TRAVELERS:

Convert expressions such as:

"2 people" → 2
"two people" → 2
"family of four" → 4
"me and my friend" → 2

BUDGET:

Preserve the numerical amount.

Examples:

"AED 8000"
→ budget = 8000
→ currency = AED

"€2000"
→ budget = 2000
→ currency = EUR

"$3000"
→ budget = 3000
→ currency = USD

"₹50000"
→ budget = 50000
→ currency = INR

"5000 GBP"
→ budget = 5000
→ currency = GBP

If the user does not specify a currency, do not invent one.

If information is missing, return null where allowed.

Return ONLY the structured TravelRequirements object.
"""

    print("\n===== REQUIREMENT AGENT =====")
    print("Extracting travel requirements...")

    result = structured_llm.invoke(prompt)

    print("Requirements extracted:")
    print(result)

    return result