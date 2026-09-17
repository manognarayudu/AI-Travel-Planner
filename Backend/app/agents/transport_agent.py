from app.llm.client import llm
from app.graph.state import TravelState


def transport_agent(state: TravelState) -> dict:
    """
    Researches practical transportation options for the destination.

    The agent focuses primarily on transportation within the destination
    and can also mention airport/arrival transfer options.
    """

    destination = state.get("destination", "")
    duration_days = state.get("duration_days") or 1
    travelers = state.get("travelers") or 1
    currency = state.get("currency") or "UNKNOWN"

    preferences = state.get("preferences", [])
    constraints = state.get("constraints", [])

    prompt = f"""
You are the Transport Agent in an Agentic AI Travel Planning System.

Research practical transportation options for the EXACT destination
provided below.

==================================================
TRIP INFORMATION
==================================================

Destination:
{destination}

Trip Duration:
{duration_days} days

Travelers:
{travelers}

Currency:
{currency}

Preferences:
{preferences}

Constraints:
{constraints}

==================================================
IMPORTANT
==================================================

The destination is:

{destination}

You MUST provide transportation information specifically for
{destination}.

Never replace the destination with another city or country.

Never assume the destination is Dubai.

Never assume the destination is Tokyo.

==================================================
TRANSPORTATION SCOPE
==================================================

Focus primarily on transportation DURING the trip, including
transportation between attractions.

Consider relevant options such as:

- Metro / subway
- Bus
- Tram
- Train
- Taxi
- Ride-hailing
- Rental car
- Bicycle
- Walking
- Ferry / boat
- Airport transfer

Only include transportation types that are actually relevant
to {destination}.

You may mention flights or intercity transportation only as an
OPTIONAL ARRIVAL/DEPARTURE consideration.

Do NOT make an expensive airline flight the recommended local
transportation option.

==================================================
COST RULES
==================================================

Provide approximate costs.

Use the requested currency:

{currency}

Do not claim live prices.

Do not claim live availability.

Do not invent exact current fares.

If exact prices are uncertain, clearly say that the prices are
approximate.

For per-ride prices, clearly label them as per ride.

For daily prices, clearly label them as per day.

For pass prices, clearly label them as approximate pass prices.

Do NOT automatically multiply every transport price by the number
of travelers unless the price is explicitly per person.

==================================================
RECOMMENDATION
==================================================

Identify the most practical transportation approach for a typical
traveler visiting {destination}.

The recommendation should consider:

- Cost
- Convenience
- Coverage
- Typical tourist usage
- Trip duration
- Flexibility

Do not make a recommendation based only on price.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY the following structure:

DESTINATION:
{destination}

TRANSPORT_OPTION_1:
TYPE:
APPROXIMATE_COST:
COST_UNIT:
SUITABLE_FOR:
ADVANTAGES:
LIMITATIONS:

TRANSPORT_OPTION_2:
TYPE:
APPROXIMATE_COST:
COST_UNIT:
SUITABLE_FOR:
ADVANTAGES:
LIMITATIONS:

TRANSPORT_OPTION_3:
TYPE:
APPROXIMATE_COST:
COST_UNIT:
SUITABLE_FOR:
ADVANTAGES:
LIMITATIONS:

TRANSPORT_OPTION_4:
TYPE:
APPROXIMATE_COST:
COST_UNIT:
SUITABLE_FOR:
ADVANTAGES:
LIMITATIONS:

RECOMMENDED_OPTION:
Name/type of the most practical option

RECOMMENDATION_REASON:
Short explanation

ESTIMATED_LOCAL_TRANSPORT_COST:
Approximate total local transportation cost for the trip for
{travelers} travelers.

ESTIMATED_CURRENCY:
{currency}

ARRIVAL_TRANSFER_NOTE:
Brief note about airport/station arrival transportation if relevant.

FINAL_NOTE:
State that prices, schedules, and availability are approximate.

Remember:

Destination = {destination}

Do not substitute another destination.
"""

    print("\n===== TRANSPORT AGENT =====")
    print("Researching transport options...")

    response = llm.invoke(prompt)

    research = response.content.strip()

    print("Transport research completed.")

    return {
        "transport_options": [
            {
                "research": research
            }
        ]
    }