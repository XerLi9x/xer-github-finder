
import requests


GITHUB_API = "https://api.github.com/search/repositories"


class GitHubSearchError(Exception):
    """Custom error for GitHub search problems."""
    pass


def search_repositories(
    query,
    language=None,
    min_stars=0,
    sort="stars",
    per_page=10
):
    """
    Search GitHub repositories.

    Args:
        query: Search keywords
        language: Programming language filter
        min_stars: Minimum repository stars
        sort: stars or updated
        per_page: Number of results (1-100)
    """

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if min_stars < 0:
        raise ValueError("Minimum stars cannot be negative.")

    if sort not in ("stars", "updated"):
        raise ValueError("Sort must be stars or updated.")

    per_page = max(1, min(int(per_page), 100))

    # Build GitHub search query
    search_query = query.strip()

    if language:
        search_query += f" language:{language.strip()}"

    if min_stars > 0:
        search_query += f" stars:>={min_stars}"

    params = {
        "q": search_query,
        "sort": sort,
        "order": "desc",
        "per_page": per_page
    }

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Xer-GitHub-Finder"
    }

    try:
        response = requests.get(
            GITHUB_API,
            params=params,
            headers=headers,
            timeout=20
        )

        if response.status_code == 403:
            raise GitHubSearchError(
                "GitHub API rate limit reached or access forbidden."
            )

        if response.status_code == 422:
            raise GitHubSearchError(
                "GitHub rejected the search query."
            )

        response.raise_for_status()

        data = response.json()

        repositories = []

        for repo in data.get("items", []):
            repositories.append({
                "name": repo.get("full_name"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "url": repo.get("html_url"),
                "updated": repo.get("updated_at"),
                "owner": repo.get("owner", {}).get("login")
            })

        return repositories

    except requests.exceptions.Timeout:
        raise GitHubSearchError("GitHub request timed out.")

    except requests.exceptions.ConnectionError:
        raise GitHubSearchError("Could not connect to GitHub.")

    except requests.exceptions.HTTPError as error:
        raise GitHubSearchError(
            f"GitHub HTTP error: {error}"
        )

    except requests.exceptions.RequestException as error:
        raise GitHubSearchError(
            f"Request failed: {error}"
        )

