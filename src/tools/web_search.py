from duckduckgo_search import DDGS
from pydantic import BaseModel

from src.config import WEB_SEARCH_MAX_RESULTS

class SearchResult(BaseModel):
    """
    A search result from DuckDuckGo Search (DDGS).
    """
    title: str
    href: str
    body: str

def web_search(
        query: str,
        max_results: int = WEB_SEARCH_MAX_RESULTS
    ) -> str:
    """
    Search the web using DuckDuckGo Search (DDGS) and return the results.

    Args:
        query (str): The search query.
        max_results (int, optional): The maximum number of results to return. Defaults to WEB_SEARCH_MAX_RESULTS.

    Returns:
        list[SearchResult]: A list of search results.
    """
    results_list = DDGS().text(
        keywords=query,
        max_results=max_results 
    )

    search_results = [SearchResult(**result) for result in results_list]
    
    # Format the search results as a string
    formatted_results = []
    for result in search_results:
        formatted_result = result.title + "\n" + result.href + "\n" + result.body + "\n"
        formatted_results.append(formatted_result)

    return "~~~~~~~~~~~~~~~~~".join(formatted_results)
