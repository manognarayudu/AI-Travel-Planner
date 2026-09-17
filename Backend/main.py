from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.graph.graph import travel_graph


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Travel Planner",
    description="Agentic AI Travel Planning and Itinerary Optimization System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://ai-travel-planner-manognya.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class TravelPlanRequest(BaseModel):
    query: str


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI Travel Planner API is running",
        "status": "success",
    }


# ============================================================
# TRAVEL PLANNING ENDPOINT
# ============================================================

@app.post("/api/plan")
def create_travel_plan(request: TravelPlanRequest):

    print("\n========================================")
    print("NEW TRAVEL PLANNING REQUEST")
    print("========================================")
    print(request.query)

    try:

        # ====================================================
        # INITIAL GRAPH STATE
        # ====================================================

        initial_state = {
            "user_query": request.query
        }

        # ====================================================
        # RUN LANGGRAPH
        # ====================================================

        result = travel_graph.invoke(initial_state)

        # ====================================================
        # TRIP REQUIREMENTS
        # ====================================================

        destination = result.get(
            "destination",
            ""
        )

        duration_days = result.get(
            "duration_days",
            0
        )

        travelers = result.get(
            "travelers",
            1
        )

        budget = result.get(
            "budget",
            0
        )

        currency = result.get(
            "currency",
            "UNKNOWN"
        )

        preferences = result.get(
            "preferences",
            []
        )

        constraints = result.get(
            "constraints",
            []
        )

        # ====================================================
        # DESTINATION
        # ====================================================

        destination_info = result.get(
            "destination_info",
            {}
        )

        # ====================================================
        # ACCOMMODATION
        # ====================================================

        accommodation_options = result.get(
            "accommodation_options",
            []
        )

        accommodation_cost = result.get(
            "accommodation_cost",
            0
        )

        # ====================================================
        # TRANSPORT
        # ====================================================

        transport_options = result.get(
            "transport_options",
            []
        )

        transport_cost = result.get(
            "transport_cost",
            0
        )

        # ====================================================
        # WEATHER
        # ====================================================

        weather = result.get(
            "weather",
            {}
        )

        # ====================================================
        # OTHER COSTS
        # ====================================================

        food_cost = result.get(
            "food_cost",
            0
        )

        activities_cost = result.get(
            "activities_cost",
            0
        )

        miscellaneous_cost = result.get(
            "miscellaneous_cost",
            0
        )

        # ====================================================
        # TOTAL BUDGET
        # ====================================================

        estimated_cost = result.get(
            "estimated_cost",
            0
        )

        budget_remaining = result.get(
            "budget_remaining",
            0
        )

        budget_status = result.get(
            "budget_status",
            "UNKNOWN"
        )

        # ====================================================
        # ITINERARY
        # ====================================================

        itinerary = result.get(
            "itinerary",
            []
        )

        # ====================================================
        # OPTIMIZATION
        # ====================================================

        optimized_itinerary = result.get(
            "optimized_itinerary",
            ""
        )

        optimization_status = result.get(
            "optimization_status",
            "UNKNOWN"
        )

        # ====================================================
        # WARNINGS
        # ====================================================

        warnings = result.get(
            "warnings",
            []
        )

        if warnings is None:
            warnings = []

        elif isinstance(warnings, str):
            warnings = [warnings]

        elif not isinstance(warnings, list):
            warnings = [str(warnings)]

        # ====================================================
        # FINAL SAFETY CHECKS
        # ====================================================

        if estimated_cost is None:
            estimated_cost = 0

        if budget_remaining is None:
            budget_remaining = float(budget) - float(
                estimated_cost
            )

        if not budget_status or budget_status == "UNKNOWN":

            if float(estimated_cost) <= float(budget):
                budget_status = "WITHIN_BUDGET"
            else:
                budget_status = "OVER_BUDGET"

        # ====================================================
        # CLEAN API RESPONSE
        # ====================================================

        response = {

            "status": "success",

            # ------------------------------------------------
            # TRIP
            # ------------------------------------------------

            "trip": {

                "destination": destination,

                "duration_days": duration_days,

                "travelers": travelers,

                "budget": budget,

                "currency": currency,

                "preferences": preferences,

                "constraints": constraints,
            },

            # ------------------------------------------------
            # DESTINATION
            # ------------------------------------------------

            "destination_info": destination_info,

            # ------------------------------------------------
            # ACCOMMODATION
            # ------------------------------------------------

            "accommodation": {

                "options": accommodation_options,

                "estimated_cost": accommodation_cost,
            },

            # ------------------------------------------------
            # TRANSPORT
            # ------------------------------------------------

            "transport": {

                "options": transport_options,

                "estimated_cost": transport_cost,
            },

            # ------------------------------------------------
            # WEATHER
            # ------------------------------------------------

            "weather": weather,

            # ------------------------------------------------
            # BUDGET
            # ------------------------------------------------

            "budget": {

                "accommodation_cost": accommodation_cost,

                "transport_cost": transport_cost,

                "food_cost": food_cost,

                "activities_cost": activities_cost,

                "miscellaneous_cost": miscellaneous_cost,

                "total_estimated_cost": estimated_cost,

                "budget_remaining": budget_remaining,

                "budget_status": budget_status,
            },

            # ------------------------------------------------
            # ITINERARY
            # ------------------------------------------------

            "itinerary": itinerary,

            # ------------------------------------------------
            # OPTIMIZATION
            # ------------------------------------------------

            "optimization": {

                "status": optimization_status,

                "optimized_itinerary": optimized_itinerary,
            },

            "final_plan": result.get(
                "final_plan",
                {}
            ),

            # ------------------------------------------------
            # WARNINGS
            # ------------------------------------------------

            "warnings": warnings,
        }

        print("\n========================================")
        print("TRAVEL PLAN GENERATED")
        print("========================================")

        return response

    except Exception as e:

        print("\n========================================")
        print("TRAVEL PLANNING ERROR")
        print("========================================")

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )