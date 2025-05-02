# tools/tavily_search.py

import os
from typing import Annotated, List
from tavily import TavilyClient

from autogen.tools import Tool

def tavily_search(
    query: Annotated[str, "The search query string"],
    max_results: Annotated[int, "Maximum results"] = 3,
    search_depth: Annotated[str, "basic or advanced"] = "basic"
) -> List[dict]:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = client.search(query=query, max_results=max_results, search_depth=search_depth)
    return [
        {"title": r["title"], "url": r["url"], "summary": r["content"][:200] + "..."}
        for r in response.get("results", [])
    ]

tool = Tool(
    name="tavily_search",
    description="Search the internet using Tavily API for up-to-date travel information.",
    func_or_tool=tavily_search
)
