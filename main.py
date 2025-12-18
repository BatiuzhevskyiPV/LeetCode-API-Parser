import httpx
import pandas as pd
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
import asyncio
from config import HEADERS, QUERY
from models import LeaderboardResponse, RankingNode

console = Console()
API = "https://leetcode.com/graphql/"


def ask_pages() -> int:
    """Ask user for number of pages to parse; ensures input is a positive integer."""

    while True:
        value = Prompt.ask("[cyan]Pages to parse[/]")
        if value.isdigit() and int(value) > 0:
            return int(value)
        console.print("[bold red]Please enter a valid number[/]")


async def fetch_leaderboard(client: httpx.AsyncClient, page=1) -> LeaderboardResponse:
    query = QUERY
    variables = {"page": page}
    resp = await client.post(API, headers=HEADERS, json={"query": query, "variables": variables})
    resp.raise_for_status()
    leaderboard = LeaderboardResponse.model_validate(resp.json())
    return leaderboard


def resolve_country(node: RankingNode) -> str:
    country_code = node.user.profile.countryCode
    if country_code and country_code.strip():
        return country_code
    if node.dataRegion == "CN":
        return "CN"
    return "Unknown"


def normalize_for_export(node: RankingNode) -> dict:
    return {
        "username": node.user.username,
        "slug": node.user.profile.userSlug,
        "rating": node.currentRating,
        "rank": node.currentGlobalRanking,
        "region": resolve_country(node)
    }


async def main():
    """
    Main execution:
    - Get user input
    - Fetch leaderboard pages asynchronously
    - Track progress with Rich
    - Save results to Excel
    """

    pages_to_parse = ask_pages()
    users = []

    async with httpx.AsyncClient() as client:
        first_page = await fetch_leaderboard(client)

        # Limit pages to total available pages
        pages_to_parse = min(pages_to_parse, first_page.data.globalRanking.totalPages)

        with Progress(
            SpinnerColumn(spinner_name="point", style="blue"),
                TextColumn("{task.description} [dim magenta]({task.percentage:>3.0f}%)"),
                BarColumn(),
                TimeRemainingColumn()
        ) as progress:
            parsed_pages = progress.add_task("Parsing pages", total=pages_to_parse)

            # Process first page
            for node in first_page.data.globalRanking.rankingNodes:
                users.append(normalize_for_export(node))
            progress.update(parsed_pages, advance=1)

            # Process remaining pages with delay between requests
            for page in range(2, pages_to_parse + 1):
                leaderboard = await fetch_leaderboard(client, page)
                for node in leaderboard.data.globalRanking.rankingNodes:
                    users.append(normalize_for_export(node))
                progress.update(parsed_pages, advance=1)
                # Ban prevention
                await asyncio.sleep(0.7)

    df = pd.DataFrame(users)
    df.to_excel('result.xlsx', index=False)


asyncio.run(main())
