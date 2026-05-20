def route_query(query: str, tools: dict):
    query = query.lower()

    if "find" in query or "search" in query:
        return tools["search"]

    if "calculate" in query:
        return tools["calculate"]

    return None