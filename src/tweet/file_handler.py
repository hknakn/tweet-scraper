"""File handling module for Twitter scraping."""

import os
from datetime import datetime
from pathlib import Path
from rich.console import Console

# Initialize Rich console
console = Console()

class TweetFileHandler:
    """Handles file operations for saving tweets."""
    
    def __init__(self):
        """Initialize the file handler."""
        self.current_file = None
        self.current_username = None
        self.file = None

    def format_date(self):
        """Format current date for filename.
        
        Returns:
            str: Formatted date string.
        """
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def format_metrics(self, metrics):
        """Format tweet metrics for output.
        
        Args:
            metrics (dict): Dictionary containing tweet metrics.
            
        Returns:
            str: Formatted metrics string.
        """
        return (f"💬 {metrics['comments']} Comments  •  "
                f"🔄 {metrics['retweets']} Retweets  •  "
                f"❤️ {metrics['likes']} Likes  •  "
                f"👁️ {metrics['views']} Views")

    def format_timestamp(self, timestamp):
        """Format timestamp for output.
        
        Args:
            timestamp (str): ISO format timestamp.
            
        Returns:
            str: Formatted date string.
        """
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%B %d, %Y at %I:%M %p")
        except:
            return timestamp

    def initialize_file(self, username):
        """Initialize file for saving tweets.
        
        Args:
            username (str): Twitter username for the file.
        """
        try:
            self.current_username = username
            filename = f"{username}_tweets_{self.format_date()}.txt"
            self.current_file = str(Path("data/tweets") / filename)
            
            # Create data directory if it doesn't exist
            Path("data/tweets").mkdir(parents=True, exist_ok=True)
            
            # Open file in append mode
            self.file = open(self.current_file, 'a', encoding='utf-8')
            
            # Write header
            header = (
                f"📱 Tweets from @{username}\n"
                f"📅 Scraped on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n"
                f"{'─' * 80}\n\n"
            )
            self.file.write(header)
            self.file.flush()
            
        except Exception as e:
            console.print(f"[red]Error initializing file: {str(e)}[/red]")

    def save_tweet(self, tweet_data):
        """Save a single tweet to file.
        
        Args:
            tweet_data (dict): The tweet data to save.
            
        Returns:
            bool: True if save was successful, False otherwise.
        """
        try:
            if not self.file:
                raise Exception("File not initialized. Call initialize_file first.")
                
            # Format the tweet data
            formatted_tweet = (
                f"🕒 {self.format_timestamp(tweet_data['timestamp'])}\n\n"
                f"{tweet_data['text']}\n\n"
                f"{self.format_metrics(tweet_data['metrics'])}\n"
                f"{'─' * 80}\n\n"
            )
            
            # Write to file and flush immediately
            self.file.write(formatted_tweet)
            self.file.flush()
            
            return True
            
        except Exception as e:
            console.print(f"[red]Error saving tweet: {str(e)}[/red]")
            return False

    def __del__(self):
        """Clean up file handler."""
        try:
            if self.file:
                self.file.close()
        except:
            pass 