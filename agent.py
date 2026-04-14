import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

load_dotenv()

# ==========================================
# Custom Tools
# ==========================================

@tool("Web Search Tool")
def search_tool(query: str) -> str:
    """Searches the web for current, real-time NBA data using the given query.
    Returns summaries from the top search results."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    encoded_query = quote_plus(query)

    # Try DuckDuckGo HTML search
    try:
        r = requests.get(
            f'https://html.duckduckgo.com/html/?q={encoded_query}',
            headers=headers, timeout=15
        )
        soup = BeautifulSoup(r.text, 'html.parser')
        results = []
        for result in soup.find_all('div', class_='result'):
            title_elem = result.find('a', class_='result__url')
            snippet_elem = result.find('a', class_='result__snippet')
            if title_elem and snippet_elem:
                results.append(
                    f"Source: {title_elem.text.strip()}\n"
                    f"Summary: {snippet_elem.text.strip()}\n"
                )
            if len(results) >= 7:
                break
        if results:
            return "\n".join(results)
    except Exception:
        pass

    # Fallback: Google search scraping
    try:
        r = requests.get(
            f'https://www.google.com/search?q={encoded_query}',
            headers=headers, timeout=15
        )
        soup = BeautifulSoup(r.text, 'html.parser')
        results = []
        for div in soup.find_all('div'):
            text = div.get_text(strip=True)
            if 80 < len(text) < 500:
                results.append(text)
            if len(results) >= 5:
                break
        if results:
            return "\n".join(results)
    except Exception:
        pass

    return "No results found for this query. Try different keywords."



# ==========================================
# Main Process Function
# ==========================================

def process(query, temperature=0.3, num_teams=5, depth="Standard"):
    """
    Runs the CrewAI NBA Championship prediction pipeline.

    Args:
        query: User's question about NBA predictions
        temperature: LLM creativity (0.0–1.0)
        num_teams: Number of teams to research
        depth: Analysis detail — "Quick", "Standard", or "Deep"

    Returns:
        Final analysis result as a string (Markdown formatted)
    """
    llm = LLM(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        base_url=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=temperature,
    )

    detail = {
        "Quick": "Provide a concise overview focusing on key insights only",
        "Standard": "Provide a thorough, well-structured analysis",
        "Deep": "Provide an exhaustive, deep-dive analysis with granular statistical detail",
    }.get(depth, "Provide a thorough, well-structured analysis")

    # ---- Agent Definitions ----
    expert = Agent(
        role="Elite NBA Analyst & Sports Writer",
        goal=(
            f"Research live data on the top {num_teams} NBA championship contenders for the "
            f"current 2025-26 season, analyze their probability, and write a compelling prediction."
        ),
        backstory=(
            "You are an award-winning NBA expert at ESPN. You excel at quickly scraping live "
            "win-loss records and stats, running advanced analytical comparisons in your head, "
            "and instantly drafting polished, engaging sports columns. You are concise and authoritative."
        ),
        llm=llm,
        verbose=True,
        max_iter=2,
        tools=[search_tool],
    )

    # ---- Task Definitions ----
    task1 = Task(
        description=(
            f"Address the user's query: '{query}'. "
            f"1. Use search_tool to find CURRENT 2025-26 NBA season data for the top {num_teams} contenders. "
            f"2. {detail} "
            f"3. Write a compelling, data-backed ESPN-style prediction article (approx 400-500 words). "
            f"Format the final output strictly in Markdown with clear headings and bullet points where appropriate."
        ),
        expected_output=(
            "A single, polished NBA championship prediction article in Markdown, combining live data research, "
            "analytics, and professional sports writing."
        ),
        agent=expert,
    )

    # ---- Execute Crew ----
    crew = Crew(
        agents=[expert],
        tasks=[task1],
        process=Process.sequential,
    )

    result = crew.kickoff(inputs={"topic": query})
    return str(result)
