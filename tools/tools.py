from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_travily_linkedin(name: str):
    """Searches for Linkedin profile Page URL."""
    search = TavilySearchResults()
    res = search.run(f"{name}")

    for result in res:
        if result["url"].startswith("https://www.linkedin.com/in/"):
            return result["url"]

    return res[0]["url"]


def get_profile_url_travily_twitter(name: str):
    """Searches for Twitter profile Page URL. Extracts the username from the Twitter URL."""
    search = TavilySearchResults()
    res = search.run(f"{name}")

    for result in res:
        if result["url"].startswith("https://twitter.com/"):
            # Extract the username part from the URL
            username = result["url"].split("/")[-1]
            # Skip if the username contains the pattern "Extract"
            if "Extract" in username or username.isdigit():
                continue
            # Construct the Twitter profile URL
            twitter_url = f"https://twitter.com/{username}"
            return twitter_url

    return res[0]["url"]
# TODO: Write tool for twitter profile page URL

