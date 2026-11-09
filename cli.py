\
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich import box

from github_search import search_repositories, GitHubSearchError


console = Console()


def show_banner():
    banner = r"""
 __  __ _____ ____  
 \ \/ /| ____|  _ \ 
  \  / |  _| | |_) |
  /  \ | |___|  _ <
 /_/\_\|_____|_| \_\

       GITHUB FINDER
    """

    console.print(
        Panel(
            Text(banner, style="bold cyan", justify="center"),
            border_style="cyan",
            padding=(1, 2)
        )
    )


def get_search_settings():
    console.print("\n[bold cyan]SEARCH SETTINGS[/bold cyan]\n")

    query = Prompt.ask(
        "[yellow]Search keywords[/yellow]"
    )

    language = Prompt.ask(
        "[yellow]Programming language[/yellow]",
        default=""
    )

    min_stars = IntPrompt.ask(
        "[yellow]Minimum Stars[/yellow]",
        default=0
    )

    sort = Prompt.ask(
        "[yellow]Sort results[/yellow]",
        choices=["stars", "updated"],
        default="stars"
    )

    per_page = IntPrompt.ask(
        "[yellow]Number of results (1-100)[/yellow]",
        default=10
    )

    return query, language or None, min_stars, sort, per_page


def display_results(results):
    if not results:
        console.print(
            "\n[yellow]No repositories found.[/yellow]"
        )
        return

    table = Table(
        title="GitHub Search Results",
        box=box.ROUNDED,
        show_lines=True,
        header_style="bold cyan"
    )

    table.add_column("#", justify="center", width=4)
    table.add_column("Repository", style="bold green")
    table.add_column("Language", style="yellow")
    table.add_column("Stars", justify="right")
    table.add_column("Description", max_width=45)
    table.add_column("URL", style="blue")

    for index, repo in enumerate(results, 1):
        description = repo["description"] or "No description"

        table.add_row(
            str(index),
            repo["name"] or "Unknown",
            repo["language"] or "Unknown",
            str(repo["stars"]),
            description,
            repo["url"] or ""
        )

    console.print()
    console.print(table)

    console.print(
        f"\n[bold green]Found {len(results)} repositories![/bold green]"
    )


def main():
    show_banner()

    try:
        query, language, min_stars, sort, per_page = (
            get_search_settings()
        )

        console.print(
            "\n[bold cyan]Searching GitHub...[/bold cyan]\n"
        )

        with console.status(
            "[cyan]Connecting to GitHub API...",
            spinner="dots"
        ):
            results = search_repositories(
                query=query,
                language=language,
                min_stars=min_stars,
                sort=sort,
                per_page=per_page
            )

        display_results(results)

    except (GitHubSearchError, ValueError) as error:
        console.print(
            f"\n[bold red]ERROR:[/bold red] {error}"
        )

    except KeyboardInterrupt:
        console.print("\n[yellow]Search cancelled.[/yellow]")


if __name__ == "__main__":
    main()

