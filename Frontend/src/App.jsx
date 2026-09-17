import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ============================================
  // SEND TRAVEL REQUEST TO BACKEND
  // ============================================
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!query.trim()) {
      setError("Please enter a travel request.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/plan`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: query.trim(),
          }),
        }
      );

      if (!response.ok) {
        let message = `Server error: ${response.status}`;

        try {
          const errorData = await response.json();

          if (errorData?.detail) {
            message = errorData.detail;
          }
        } catch {
          // Keep default error message
        }

        throw new Error(message);
      }

      const data = await response.json();

      console.log("API RESPONSE:", data);

      setResult(data);
    } catch (err) {
      console.error("API ERROR:", err);

      setError(
        `Unable to generate the travel plan: ${
          err.message || "Unknown error"
        }`
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================
  // CONVERT LLM / API DATA INTO CLEAN TEXT
  // ============================================
  const cleanText = (value) => {
    if (value === null || value === undefined) {
      return "";
    }

    // Arrays
    if (Array.isArray(value)) {
      return value
        .map((item) => cleanText(item))
        .filter(Boolean)
        .join("\n\n");
    }

    // Objects
    if (typeof value === "object") {
      if (value.research) {
        return cleanText(value.research);
      }

      if (value.plan) {
        return cleanText(value.plan);
      }

      if (value.text) {
        return cleanText(value.text);
      }

      if (value.content) {
        return cleanText(value.content);
      }

      if (value.final_plan) {
        return cleanText(value.final_plan);
      }

      if (value.optimized_itinerary) {
        return cleanText(value.optimized_itinerary);
      }

      return JSON.stringify(value, null, 2);
    }

    let text = String(value);

    // Fix escaped characters
    text = text
      .replace(/\\n/g, "\n")
      .replace(/\\"/g, '"')
      .replace(/\\'/g, "'")
      .replace(/\r/g, "");

    // Remove surrounding quotes
    if (
      text.startsWith('"') &&
      text.endsWith('"')
    ) {
      text = text.slice(1, -1);
    }

    // Remove common Markdown formatting
    text = text
      .replace(/\*\*(.*?)\*\*/g, "$1")
      .replace(/__(.*?)__/g, "$1")
      .replace(/`(.*?)`/g, "$1");

    return text.trim();
  };

  // ============================================
  // CLEAN RESEARCH DISPLAY
  // ============================================
  const renderResearch = (value) => {
    const text = cleanText(value);

    if (!text) {
      return (
        <p className="empty-message">
          Information unavailable.
        </p>
      );
    }

    // Detect OPTION 1 / OPTION_1 / OPTION-1
    const optionParts = text.split(
      /(?=OPTION[_\s-]*\d+\s*:)/i
    );

    if (optionParts.length > 1) {
      return (
        <div className="research-options">
          {optionParts.map((option, index) => (
            <div
              className="research-option"
              key={index}
            >
              <div className="option-number">
                {index + 1}
              </div>

              <div className="option-content">
                {option
                  .trim()
                  .split("\n")
                  .map((line, i) => {
                    const cleanedLine = line
                      .replace(
                        /^OPTION[_\s-]*\d+\s*:\s*/i,
                        ""
                      )
                      .trim();

                    if (!cleanedLine) {
                      return (
                        <div
                          key={i}
                          className="text-gap"
                        />
                      );
                    }

                    return (
                      <p key={i}>
                        {cleanedLine}
                      </p>
                    );
                  })}
              </div>
            </div>
          ))}
        </div>
      );
    }

    return (
      <div className="clean-research">
        {text.split("\n").map((line, index) => {
          const trimmed = line.trim();

          if (!trimmed) {
            return (
              <div
                key={index}
                className="text-gap"
              />
            );
          }

          const isHeading =
            /^[A-Z][A-Z0-9 _-]{2,}:?$/.test(
              trimmed
            );

          if (isHeading) {
            return (
              <h4 key={index}>
                {trimmed.replace(/:$/, "")}
              </h4>
            );
          }

          return (
            <p key={index}>
              {trimmed}
            </p>
          );
        })}
      </div>
    );
  };

  // ============================================
  // ITINERARY DISPLAY
  // ============================================
  const renderItinerary = (value) => {
    let text = cleanText(value);

    if (!text) {
      return (
        <p className="empty-message">
          Itinerary information unavailable.
        </p>
      );
    }

    // Fix escaped newlines again after object conversion
    text = text
      .replace(/\\n/g, "\n")
      .replace(/\r/g, "");

    // Remove optimization metadata
    text = text
      .replace(
        /OPTIMIZATION_STATUS\s*:\s*[^\n]*/gi,
        ""
      )
      .replace(
        /OPTIMIZATION_NOTES\s*:[\s\S]*?(?=DAY\s*\d+|$)/gi,
        ""
      );

    // Remove final warnings from itinerary
    text = text
      .split(
        /FINAL[_\s-]*WARNINGS\s*:/i
      )[0]
      .trim();

    /*
      VERY IMPORTANT:

      This catches all of these:

      DAY 1
      DAY 1:
      Day 1
      Day 1:
      **DAY 1:**
      **Day 2**
      DAY 3 -
      DAY 4:
    */

    const dayRegex =
      /(?:\*\*)?\s*DAY\s*(\d+)\s*(?:\*\*)?\s*:?\s*(?:[-–—]\s*)?/gi;

    const matches = [
      ...text.matchAll(dayRegex),
    ];

    // If no DAY headings were found
    if (matches.length === 0) {
      return (
        <div className="itinerary-text">
          {text}
        </div>
      );
    }

    // Create separate day objects
    const days = matches.map(
      (match, index) => {
        const dayNumber = match[1];

        const start =
          match.index + match[0].length;

        const end =
          index + 1 < matches.length
            ? matches[index + 1].index
            : text.length;

        let content = text
          .slice(start, end)
          .trim();

        // Remove leftover Markdown
        content = content
          .replace(/\*\*/g, "")
          .replace(/^[-–—]\s*/, "")
          .trim();

        return {
          dayNumber,
          content,
        };
      }
    );

    return (
      <div className="itinerary-days">
        {days.map((day, index) => (
          <div
            className="day-card"
            key={`${day.dayNumber}-${index}`}
          >
            {/* DAY NUMBER */}
            <div className="day-number">
              {day.dayNumber}
            </div>

            {/* DAY CONTENT */}
            <div className="day-content">
              <h4>
                Day {day.dayNumber}
              </h4>

              <div className="day-text">
                {day.content
                  .split("\n")
                  .map((line, i) => {
                    let trimmed =
                      line.trim();

                    // Empty line
                    if (!trimmed) {
                      return (
                        <div
                          key={i}
                          className="itinerary-gap"
                        />
                      );
                    }

                    // Remove Markdown bold
                    trimmed =
                      trimmed.replace(
                        /\*\*/g,
                        ""
                      );

                    // Morning / Afternoon / Evening
                    if (
                      /^(Morning|Afternoon|Evening)\s*:?\s*$/i.test(
                        trimmed
                      )
                    ) {
                      return (
                        <div
                          key={i}
                          className="time-heading"
                        >
                          {trimmed.replace(
                            /:$/,
                            ""
                          )}
                        </div>
                      );
                    }

                    // Lines such as:
                    // Morning: Visit...
                    // Afternoon: Explore...
                    const timeLineMatch =
                      trimmed.match(
                        /^(Morning|Afternoon|Evening)\s*:\s*(.+)$/i
                      );

                    if (timeLineMatch) {
                      return (
                        <div
                          key={i}
                          className="itinerary-line"
                        >
                          <strong>
                            {
                              timeLineMatch[1]
                            }
                            :
                          </strong>{" "}
                          {
                            timeLineMatch[2]
                          }
                        </div>
                      );
                    }

                    return (
                      <div
                        key={i}
                        className="itinerary-line"
                      >
                        {trimmed}
                      </div>
                    );
                  })}
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  // ============================================
  // CURRENCY
  // ============================================
  const currency =
    result?.trip?.currency || "";

  // ============================================
  // UI
  // ============================================
  return (
    <div className="app">

      {/* ======================================
          HERO
          ====================================== */}
      <header className="hero">
        <div className="hero-content">

          <div className="badge">
            ✦ AI-POWERED TRAVEL PLANNER
          </div>

          <h1>
            Plan your perfect
            <span>
              journey with AI.
            </span>
          </h1>

          <p>
            Tell us where you want to go, your
            budget and preferences. Our
            intelligent travel agents will create
            and optimize your complete travel
            plan.
          </p>

        </div>
      </header>

      <main className="container">

        {/* ====================================
            TRAVEL INPUT
            ==================================== */}
        <section className="planner-card">

          <span className="section-label">
            TRAVEL PLANNER
          </span>

          <h2>
            Where are you going?
          </h2>

          <p>
            Describe your trip naturally. Our AI
            will understand the destination,
            duration, travelers and budget.
          </p>

          <form onSubmit={handleSubmit}>

            <textarea
              value={query}
              onChange={(e) =>
                setQuery(e.target.value)
              }
              placeholder="Example: Plan a 5-day trip to Dubai for two people with a budget of AED 8000..."
              rows="5"
            />

            <div className="form-bottom">

              <span className="hint">
                💡 Try any destination, currency
                or budget
              </span>

              <button
                type="submit"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Generating...
                  </>
                ) : (
                  <>
                    Generate Travel Plan
                    <span>→</span>
                  </>
                )}
              </button>

            </div>

          </form>

          {error && (
            <div className="error">
              ⚠ {error}
            </div>
          )}

        </section>

        {/* ====================================
            LOADING
            ==================================== */}
        {loading && (
          <section className="loading-card">

            <div className="loading-icon">
              ✦
            </div>

            <h3>
              Creating your travel plan...
            </h3>

            <p>
              Our AI agents are researching your
              destination, accommodation,
              transportation, weather, budget
              and itinerary.
            </p>

            <div className="agent-progress">
              <span>Destination</span>
              <span>Accommodation</span>
              <span>Transport</span>
              <span>Weather</span>
              <span>Budget</span>
              <span>Itinerary</span>
            </div>

          </section>
        )}

        {/* ====================================
            RESULTS
            ==================================== */}
        {result && !loading && (
          <section className="results">

            {/* RESULT HEADER */}
            <div className="results-title">

              <div>
                <span className="section-label">
                  YOUR AI-GENERATED PLAN
                </span>

                <h2>
                  {result.trip?.destination ||
                    "Your Trip"}
                </h2>
              </div>

              <div className="status-pill">
                ● Plan Generated
              </div>

            </div>

            {/* =================================
                TRIP OVERVIEW
                ================================= */}
            <div className="overview-grid">

              <div className="overview-card">
                <span>📅</span>

                <div>
                  <small>
                    Duration
                  </small>

                  <strong>
                    {result.trip
                      ?.duration_days ||
                      "-"}{" "}
                    days
                  </strong>
                </div>
              </div>

              <div className="overview-card">
                <span>👥</span>

                <div>
                  <small>
                    Travelers
                  </small>

                  <strong>
                    {result.trip
                      ?.travelers ||
                      "-"}{" "}
                    people
                  </strong>
                </div>
              </div>

              <div className="overview-card">
                <span>💰</span>

                <div>
                  <small>
                    Budget
                  </small>

                  <strong>
                    {result.trip?.budget ||
                      "-"}{" "}
                    {currency}
                  </strong>
                </div>
              </div>

              <div className="overview-card">
                <span>✓</span>

                <div>
                  <small>
                    Budget Status
                  </small>

                  <strong>
                    {result.budget
                      ?.budget_status ||
                      "N/A"}
                  </strong>
                </div>
              </div>

            </div>

            {/* =================================
                BUDGET
                ================================= */}
            <div className="result-section">

              <span className="section-label">
                COST BREAKDOWN
              </span>

              <h3>
                Trip Budget
              </h3>

              <div className="budget-grid">

                <div className="budget-item">
                  <span>
                    🏨 Accommodation
                  </span>

                  <strong>
                    {result.budget
                      ?.accommodation_cost ||
                      0}{" "}
                    {currency}
                  </strong>
                </div>

                <div className="budget-item">
                  <span>
                    🚕 Transport
                  </span>

                  <strong>
                    {result.budget
                      ?.transport_cost ||
                      0}{" "}
                    {currency}
                  </strong>
                </div>

                <div className="budget-item">
                  <span>
                    🍴 Food
                  </span>

                  <strong>
                    {result.budget
                      ?.food_cost ||
                      0}{" "}
                    {currency}
                  </strong>
                </div>

                <div className="budget-item">
                  <span>
                    🎟 Activities
                  </span>

                  <strong>
                    {result.budget
                      ?.activities_cost ||
                      0}{" "}
                    {currency}
                  </strong>
                </div>

                <div className="budget-item">
                  <span>
                    🧳 Miscellaneous
                  </span>

                  <strong>
                    {result.budget
                      ?.miscellaneous_cost ||
                      0}{" "}
                    {currency}
                  </strong>
                </div>

              </div>

              <div className="budget-total">

                <div>
                  <span>
                    Total Estimated Cost
                  </span>

                  <strong>
                    {result.budget
                      ?.total_estimated_cost ||
                      0}{" "}
                    {currency}
                  </strong>
                </div>

                <div>
                  <span>
                    Remaining Budget
                  </span>

                  <strong>
                    {result.budget
                      ?.budget_remaining ||
                      0}{" "}
                    {currency}
                  </strong>
                </div>

              </div>

            </div>

            {/* =================================
                DESTINATION RESEARCH
                ================================= */}
            <div className="result-section">

              <span className="section-label">
                DESTINATION RESEARCH
              </span>

              <h3>
                Discover{" "}
                {result.trip?.destination}
              </h3>

              <div className="research-box">
                {renderResearch(
                  result.destination_info
                )}
              </div>

            </div>

            {/* =================================
                ACCOMMODATION
                ================================= */}
            <div className="result-section">

              <span className="section-label">
                STAY
              </span>

              <h3>
                Accommodation Options
              </h3>

              <div className="research-box">
                {renderResearch(
                  result.accommodation
                    ?.options
                )}
              </div>

            </div>

            {/* =================================
                TRANSPORT
                ================================= */}
            <div className="result-section">

              <span className="section-label">
                GETTING AROUND
              </span>

              <h3>
                Transportation
              </h3>

              <div className="research-box">
                {renderResearch(
                  result.transport
                    ?.options
                )}
              </div>

            </div>

            {/* =================================
                WEATHER
                ================================= */}
            <div className="result-section">

              <span className="section-label">
                WEATHER
              </span>

              <h3>
                Weather Information
              </h3>

              <div className="research-box">
                {renderResearch(
                  result.weather
                )}
              </div>

            </div>

            {/* =================================
                ITINERARY
                ================================= */}
            <div className="result-section itinerary-section">

              <span className="section-label">
                DAY-BY-DAY PLAN
              </span>

              <h3>
                Your Itinerary
              </h3>

              <div className="itinerary-box">

                {renderItinerary(
                  result.optimization
                    ?.final_plan ||
                  result.optimization
                    ?.optimized_itinerary ||
                  result.itinerary
                )}

              </div>

            </div>

            {/* =================================
                OPTIMIZATION
                ================================= */}
            <div className="optimization-card">

              <div className="optimization-icon">
                ✦
              </div>

              <div>

                <span className="section-label">
                  AI OPTIMIZATION
                </span>

                <h3>
                  Itinerary Optimized
                </h3>

                <p>
                  The itinerary was reviewed by
                  the optimization agent for
                  budget, feasibility, travel
                  time and scheduling consistency.
                </p>

              </div>

            </div>

            {/* =================================
                WARNINGS
                ================================= */}
            {result.warnings &&
              result.warnings.length > 0 && (
                <div className="warning-card">

                  <h3>
                    ⚠ Important Notes
                  </h3>

                  {result.warnings.map(
                    (warning, index) => (
                      <p key={index}>
                        • {warning}
                      </p>
                    )
                  )}

                </div>
              )}

            {/* =================================
                PLAN ANOTHER TRIP
                ================================= */}
            <div className="new-plan">

              <button
                onClick={() => {
                  setResult(null);
                  setQuery("");
                  setError("");

                  window.scrollTo({
                    top: 0,
                    behavior: "smooth",
                  });
                }}
              >
                ← Plan Another Trip
              </button>

            </div>

          </section>
        )}

      </main>

      {/* ======================================
          FOOTER
          ====================================== */}
      <footer>
        <p>
          AI Travel Planner • Agentic AI Travel
          Planning & Itinerary Optimization
          System
        </p>
      </footer>

    </div>
  );
}

export default App;