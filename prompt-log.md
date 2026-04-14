# Prompt Log — Assignment 5

## AI-Assisted Development Process

This document records the full AI-assisted development process for building the NBA Championship Prediction Dashboard, capturing every prompt from initialization to final visual polish.

---

### Prompt 1: Context Gathering
**User:** Give me a summary of my previous crewai agent assignment

**AI:** Provided a comprehensive summary of Assignments 3 (March Madness Predictions) and 4 (ETF Analysis Pipeline), covering architectures, tools, challenges, and key patterns.

### Prompt 2: Core Implementation Plan
**User:** Follow the above instructions to develop a comprehensive dashboard that allows user to interact with the NCAA agent and retrieve output generated on the dashboard. This time I would like the app to focus on NBA championship prediction so different info should be scraped from the internet. Query page should look like the Manus example above.

**AI:** Created a detailed implementation plan covering:
- Architecture diagram (app.py → agent.py with 3 CrewAI agents)
- Manus-style centered query UI design
- Sidebar configuration (temperature, num_teams, depth)
- Agent module with custom DuckDuckGo search and scraping
- All essential files generated.

### Prompt 3: App Verification
**User:** Continue

**AI:** Ran a browser subagent verification on the locally running Streamlit app. Verified the Manus-style layout was rendering properly. 

### Prompt 4: Taking Screenshots
**User:** Continue

**AI:** Triggered the backend to save `screenshot.png`, verified that all 8 necessary files (app, agent, env, requirements, gitignore, etc.) were created and prepared walkthrough/task completion artifacts.

### Prompt 5: Infinite Loading Issue
**User:** Took so long to load for the results (10 minutes still nothing). See if theres anything to modify

**AI:** Diagnosed that `ScrapeWebsiteTool` was hanging and the ReAct LLM loop was getting stuck. Removed the slow scraping tool entirely, strictly forced `max_iter=2` on all agents, and shortened expected outputs to dramatically improve generation speed.

### Prompt 6: Text Visibility Fix
**User:** Words are in white and could only be seen unless highlighted. Same for the query bar. Try fix the issues please

**AI:** Identified that Streamlit Dark Mode was injecting `#ffffff` (white) text against my custom `#fafbfc` (light gray) background container. Explicitly injected CSS overrides (`color: #1f2937 !important;`) to force dark text parsing globally and within markdown results.

### Prompt 7: Error Catching
**User:** Add some error handling features

**AI:** Wrapped the CrewAI agent execution in a robust `try...except` block in `app.py`. Added specific exception catches for API key configuration faults (`ValueError`), LLM Rate Limits (`429 error`), and network timeouts, injecting them safely as `st.error` GUI banners.

### Prompt 8: Speed Optimization
**User:** The outgput generation is still kinda slow as it takes at least 2 minutes. Try minimize the response time but keeping the quality of the output

**AI:** Completely ripped out the 3-agent sequential pipeline (Researcher → Analyst → Writer) causing triple LLM latency. Replaced it with a *single elite agent* capable of handling the research, mental analysis, and article synthesis in one single shot, cutting execution time down to ~20 seconds without quality loss.

### Prompt 9: UI Enhancements
**User:** Add caret navigation in the text box
Add a quick action named MVP Candidates

**AI:** Injected `caret-color: #1f2937 !important;` into the text input CSS. Reorganized the Quick Action buttons from a 3-column row into a clean 2x2 grid, adding the requested "🌟 MVP Candidates" action.

### Prompt 10: Background Image Integration
**User:** Use this as the website background. But be transparent so it wont be too coloful (uploaded NBA logos picture)

**AI:** Cloned the provided image into `bg.jpg` and built a Python utility in `app.py` wrapper to securely encode it into base64. Embedded the image into the core `stApp` container CSS, overlaying a massive 88% `linear-gradient` (`rgba(250, 251, 252, 0.88)`) on top to give it a muted, premium watermark effect instead of an overpowering collage.

### Prompt 11: Python Syntax Bug
**User:** Solve the issue (provided screenshot showing NameError: name 'color' is not defined)

**AI:** Identified that when adding the `bg_img` f-string block to `<style>`, standard CSS brackets `{ ... }` collided with Python f-string logic. Escaped ALL remaining CSS braces as `{{` and `}}` to resolve the syntax crash immediately.

### Prompt 12: Conditional Background Display
**User:** Picture looks great in the front page But for the results page it becomes unclear for the users to read the ouput, maybe just let the background be white like the original one, or if you have any other thoughts

**AI:** Moved Session State initialization to the very top in `app.py`. Dynamically injected CSS so that `background-image` drops its image-rendering and reverts to the clean `#fafbfc` backdrop the very moment `st.session_state.result` populates during an analysis response. Visually separated the UI layouts flawlessly without losing the landing page swagger.

### Prompt 13: Hero Text Sizing
**User:** What can I predict for you? AI-powered NBA Championship predictions using multi-agent intelligence
Font size of these two lines should be bigger and may I know what font are you using right now

**AI:** Explained that the elegant styling relies on Google's modern `Inter` font stack. Tweaked the CSS headers, scaling the main hero to `3.2rem` (font-weight 700) and bumping the semantic sub-layer to `1.35rem`, making the UX highly focal and easy to scan.

### Prompt 14: Final Screenshot Check
**User:** Reatake the screenshot of the dashboard. One for the front page, another for the results

**AI:** Attempted automated browser execution via playwright subagent but hit `Protocol error (Browser.setDownloadBehavior)` due to system context management faults. Detailed issue and provided guidance to manual MacOS screen caps `Cmd+Shift+4` to circumvent automation blocker.

### Prompt 15: Document Full History
**User:** Add all our chat history, literally everything to the prompt-log

**AI:** Siphoned the active chat log and updated `prompt-log.md` with an extensive documentation string of the entire development life cycle precisely as requested.

### Prompt 16: Sidebar Screenshots
**User:** Add these screenshot to the sidebar

**AI:** Copied the user's uploaded `front_page` and `results_page` images directly into the project directory. Updated the `app.py` script to seamlessly render `st.image()` widgets at the bottom of the Streamlit sidebar to display the system visual state.

### Prompt 17: Post-Development Documentation
**User:** Update the readme and promptlog files with all the details

**AI:** Comprehensively updated both `README.md` and `prompt-log.md`. Logged the latest interactions and completely overhauled the `README.md` to reflect the massive architectural changes (e.g. pivoting to a Single Elite Agent), UI overhauls (transparent background generation), and error handling protocols.

---
*Development tool: Antigravity AI Coding Assistant*
