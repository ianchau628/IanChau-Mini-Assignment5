# Mini-Assignment 5: NBA Championship Prediction Dashboard

## System Overview

This project is a **Streamlit dashboard** that provides a Manus-style user interface for interacting with a CrewAI multi-agent system. The agents collaboratively research, analyze, and predict the NBA Championship winner for the 2025-26 season using real-time web data.

### Workflow

1. **User Input** — The user types a question or selects a quick-action button on the Manus-style query page.
2. **Elite Agent Pipeline** — The query is passed to a single, highly optimized **Elite NBA Analyst & Sports Writer** CrewAI agent. Why only one? By dropping the latency of passing context across 3 distinct agents, execution time plummets from 2+ minutes to mere seconds. The agent simultaneously:
   - Researches live data using a custom DuckDuckGo search tool.
   - Analytically evaluates the championship contenders.
   - Writes a polished, ESPN-style predictive column.
3. **Dynamic Results Display** — The moment the analysis returns, the UI drops the vivid translucent landing page wallpaper, replacing it with a clean minimalist background to prioritize readability.

### Key Components

| File | Purpose |
|------|---------|
| `app.py` | Streamlit dashboard (Manus-style UI, CSS injection, error handling) |
| `agent.py` | Highly-optimized single-agent CrewAI module (`process()` entry point) |
| `requirements.txt` | Python dependencies |
| `.env` | DeepSeek API key (not committed to Git) |

## How to Run

1. Create a `.env` file with your DeepSeek API key:
   ```
   DEEPSEEK_API_KEY=your_api_key_here
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```

## Features Implemented

- **Manus-style UI** — centered layout, rounded `14px` components, deep focus `color: #1f2937`, and caret-color injection.
- **Dynamic Background Rendering** — Streamlit loads an NBA-collage wallpaper embedded via `base64` natively. CSS dynamically drops the wallpaper when rendering the results page.
- **Four Quick Actions** — Buttons for "Predict Champion", "Top Contenders", "MVP Candidates," and "Playoff Preview" in a 2x2 grid.
- **Robust Error Handling** — Specific python logic to gracefully parse configuration errors, API rate limit crashes (`429`), network dropouts, and empty generation loops.
- **High-Speed Execution** — Strict `max_iter=2` agent looping completely negates the infinite re-act loops famous in CrewAI.

## Design Decisions

1. **Manus-inspired UI over default Streamlit** — Custom CSS sets `font-family: 'Inter'`, gradient buttons, and removes heavy Streamlit chrome.
2. **Single "Elite" Agent strategy** — To prevent frustrating 3-10 minute wait times and common scraping hangups, the 3-agent system was consolidated into one rapid agent, speeding up predictions exponentially.
3. **DuckDuckGo search_tool only** — Ripped out `ScrapeWebsiteTool` completely as it causes excessive timeout lagging on heavily rendered sports sites.
4. **Transparent CSS Image Overlay** — Because base Streamlit doesn't support complex opacity image layers natively, an 88% `linear-gradient` is painted over the background image inside the `.stApp` container to achieve a gorgeous muted branding.
5. **Dashboard Sidebar Attachments** — Active dashboard visual state loaded directly into the sidebars automatically.
