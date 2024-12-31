#!/usr/bin/env python3
"""Script for scraping tweets from a Twitter profile."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.text import Text

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.scraper import TwitterScraper

# Initialize Rich console
console = Console()

def main():
    """Main function for the tweet scraping script."""
    try:
        # Show welcome message
        console.print(Panel.fit(
            "[bold blue]Twitter Scraper[/bold blue]\n[dim]A tool to scrape tweets from Twitter profiles[/dim]",
            border_style="blue"
        ))
        
        # Load Twitter credentials from .env file
        with console.status("[bold blue]Loading credentials...", spinner="dots"):
            load_dotenv()
            twitter_username = os.getenv('TWITTER_USERNAME')
            twitter_password = os.getenv('TWITTER_PASSWORD')

        if not twitter_username or not twitter_password:
            console.print("\n[yellow]Twitter credentials not found in .env file![/yellow]")
            twitter_username = Prompt.ask("Enter your Twitter username or email")
            twitter_password = Prompt.ask("Enter your Twitter password", password=True)

        # Get target username
        username = Prompt.ask("\nEnter Twitter username to scrape (without @)", default="", show_default=False)
        if not username:
            console.print("[red]Username cannot be empty![/red]")
            return
            
        # Ask for headless mode
        use_headless = Confirm.ask("Run in headless mode? (browser will run in background)", default=False)
        
        # Create data directory if it doesn't exist
        data_dir = Path("data/tweets")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize scraper
        with console.status("[bold blue]Starting browser...", spinner="dots"):
            scraper = TwitterScraper(headless=use_headless)
        
        # Login to Twitter
        with console.status("[bold blue]Logging in to Twitter...", spinner="dots"):
            if not scraper.login(twitter_username, twitter_password):
                console.print("[red]Login failed. Please check your credentials.[/red]")
                scraper.close()
                return
            console.print("[green]Successfully logged in![/green]")
        
        # Scrape tweets
        console.print(f"\n[bold blue]Scraping tweets from @{username}...[/bold blue]")
        tweets = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Collecting tweets...", total=None)
            
            def update_progress(description):
                progress.update(task, description=description)
            
            tweets = scraper.get_tweets(username, progress_callback=update_progress)
            progress.update(task, completed=True)
        
        # Save results
        if tweets:
            with console.status("[bold blue]Saving tweets...", spinner="dots"):
                filename = scraper.save_tweets_to_file(tweets, username)
            
            result = Text()
            result.append("\n✨ ", style="bold yellow")
            result.append(f"Successfully saved ", style="bold green")
            result.append(str(len(tweets)), style="bold blue")
            result.append(" tweets to:\n", style="bold green")
            result.append(f"📁 {filename}", style="bold blue")
            console.print(Panel(result, border_style="green"))
        else:
            console.print("\n[yellow]No tweets were found or an error occurred.[/yellow]")
        
        # Cleanup
        with console.status("[bold blue]Cleaning up...", spinner="dots"):
            scraper.close()
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Scraping interrupted by user.[/yellow]")
        try:
            scraper.close()
        except:
            pass
            
    except Exception as e:
        console.print(f"\n[red]An error occurred: {str(e)}[/red]")

if __name__ == "__main__":
    main() 