# Travel Planner AI Assistant

A multi-agent travel planning system built using the **Autogen** framework and **Streamlit**. This app allows users to generate personalized travel itineraries with intelligent agents that collaborate based on user input.

---

## Agent Architecture

| Agent                  | Role & Responsibilities |
|------------------------|--------------------------|
| **User_Proxy_Agent**   | Initiates conversation with the user and delegates requests. |
| **Destination_Expert** | Suggests the best location based on user preferences. |
| **Itinerary_Creator**  | Creates day-by-day activity plans. |
| **Budget_Analyst**     | Estimates costs and suggests optimizations. |
| **Report_Writer**      | Compiles a complete travel report for the user. |

---

## Interaction Flow

```
User_Proxy -> Destination_Expert -> Itinerary_Creator -> Budget_Analyst -> Report_Writer
```

---

##  Features

- Agent collaboration via Autogen's `GroupChat`
- Budget pie chart visualization with Matplotlib
- Final report generation with downloadable `.txt` output
- Dynamic conversation logging & agent activity trace
- Modular and extensible architecture

---

##  Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

`.env` file required with:
```
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

---

## Docker Support

### Build Image
```bash
docker build -t travel-planner .
```

### Run Container
```bash
docker run -p 8501:8501 --name travel-agent-ui travel-planner
```

Visit: [http://localhost:8501](http://localhost:8501)

---

## Project Structure

```
├── main.py                  # Main Streamlit UI & Autogen orchestration
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image setup
├── .env                     # API keys
```

---

## Completed Capabilities

- [x] Streamlit UI for user input
- [x] 5-agent Autogen conversation pipeline
- [x] Budget parsing from LLM output
- [x] Dynamic pie chart generation
- [x] Final trip report download

---

### 🛠 Challenges & To-Do 

* [ ] **Align Tool Usage with LLM Responses**
  Although `Tool.py` works, integrating tool outputs with LLM-generated replies proved difficult.
  *→ Improvement: Enable seamless tool + LLM response merging for more natural outputs.*

* [ ] **Report Writer Integration Issues**
  Adding the `Report_Writer_Agent` led to unexpected behavior or termination.
  *→ Improvement: Diagnose and ensure smooth message handoff from Budget → Report Writer.*

* [ ] **Agent Configuration for Tools**
  Registering tools properly across agents (for LLM and execution contexts) was error-prone.
  *→ Improvement: Standardize tool registration logic per agent role.*

* [ ] **Modularization Took Time**
  Structuring code into clearly defined modules was time-consuming but critical.
  *→ Improvement: Start with isolated modules (agents, tools, UI) from the beginning.*

* [ ] **Bing API Limitation**
  Bing Search API requires payment or special access.
  *→ Improvement: Consider fallback APIs (e.g., Tavily, SerpAPI) with easier developer access.*

* [ ] **LLM-Only Mode as Fallback**
  Due to tool integration challenges, the final version relied solely on LLMs.
  *→ Improvement: Create dual-mode support (LLM-only vs LLM+Tool hybrid).*

* [ ] **Agent Feedback Mechanism (Future Feature)**
  No support for dynamic feedback like “I only have €100, please revise plan.”
  *→ Improvement: Add user-agent feedback loop for real-time itinerary/budget adjustments.*





