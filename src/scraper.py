"""Main Twitter scraping module."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .browser.browser_manager import BrowserManager
from .tweet.processor import TweetProcessor
from .tweet.file_handler import TweetFileHandler
from .config.settings import SCROLL_SETTINGS

# Initialize Rich console
console = Console()

class TwitterScraper:
    """Main class for scraping Twitter profiles."""
    
    def __init__(self, headless=False):
        """Initialize the Twitter scraper.
        
        Args:
            headless (bool): Whether to run the browser in headless mode.
        """
        self.browser = BrowserManager(headless)
        self.is_logged_in = False
        self.no_new_tweets_count = 0
        self.batch_size = 20
        self.tweet_processor = TweetProcessor()
        self.file_handler = TweetFileHandler()
        self.current_username = None
        self.progress_callback = None

    def login(self, username, password):
        """Login to Twitter.
        
        Args:
            username (str): Twitter username or email.
            password (str): Twitter password.
            
        Returns:
            bool: True if login was successful, False otherwise.
        """
        self.is_logged_in = self.browser.login(username, password)
        return self.is_logged_in

    def get_tweets(self, username, progress_callback=None):
        """Optimized tweet collection with immediate saving.
        
        Args:
            username (str): The Twitter username to scrape.
            progress_callback: Callback function to update progress.
            
        Returns:
            list: List of collected tweets.
        """
        tweets = []
        consecutive_empty_scrolls = 0
        last_height = 0
        no_height_change = 0
        max_retries = SCROLL_SETTINGS['max_retries']
        self.progress_callback = progress_callback
        
        try:
            # Set the username for file naming
            self.current_username = username
            
            # Initialize file handler
            self.file_handler.initialize_file(username)
            
            # Navigate to profile and wait for initial load
            self.browser.driver.get(f"https://twitter.com/{username}")
            
            # Wait for tweets with better selector
            try:
                self.browser.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'article[role="article"]'))
                )
                self.browser.random_sleep(2, 3)
            except Exception as e:
                console.print("[red]No tweets found on profile. Please check the username.[/red]")
                return tweets

            while True:
                # Get all tweet articles directly
                tweet_elements = self.browser.driver.find_elements(By.CSS_SELECTOR, 'article[role="article"]')
                current_height = self.browser.driver.execute_script("return document.documentElement.scrollHeight")
                
                if not tweet_elements:
                    consecutive_empty_scrolls += 1
                    if consecutive_empty_scrolls >= max_retries:
                        break
                    self.browser.random_sleep(2, 3)
                    continue

                # Process all visible tweets
                new_tweets = []
                for tweet in tweet_elements:
                    tweet_data = self.process_tweet(tweet)
                    if tweet_data:
                        new_tweets.append(tweet_data)
                
                if new_tweets:
                    tweets.extend(new_tweets)
                    consecutive_empty_scrolls = 0
                    no_height_change = 0
                    
                    # Update progress with tweet count
                    if self.progress_callback:
                        self.progress_callback(f"Collecting tweets... ({len(tweets)} found)")
                else:
                    consecutive_empty_scrolls += 1
                
                # Check if we're really at the end
                if current_height == last_height:
                    no_height_change += 1
                    if no_height_change >= max_retries:
                        break
                else:
                    no_height_change = 0
                    
                last_height = current_height
                
                # Scroll with retries
                scroll_success = False
                for _ in range(max_retries):
                    if self.browser.smart_scroll():
                        scroll_success = True
                        break
                    self.browser.random_sleep(1, 2)
                
                if not scroll_success:
                    break

        except KeyboardInterrupt:
            console.print("\n[yellow]Scraping interrupted by user.[/yellow]")
            
        except Exception as e:
            console.print(f"\n[red]An error occurred: {str(e)}[/red]")
        
        return tweets

    def close(self):
        """Close the browser and clean up."""
        self.browser.close()

    def process_tweet(self, tweet):
        """Process a single tweet and save it.
        
        Args:
            tweet: The Selenium element containing the tweet.
            
        Returns:
            dict: The processed tweet data.
        """
        tweet_data = self.tweet_processor.process_tweet(tweet)
        if tweet_data:
            self._save_single_tweet(tweet_data)
        return tweet_data

    def _save_single_tweet(self, tweet_data):
        """Save a single tweet immediately after processing.
        
        Args:
            tweet_data (dict): The tweet data to save.
            
        Returns:
            bool: True if the save was successful, False otherwise.
        """
        return self.file_handler.save_tweet(tweet_data)

    def save_tweets_to_file(self, tweets, username):
        """Save tweets to a text file with optimized formatting.
        
        Args:
            tweets (list): List of tweets to save.
            username (str): The Twitter username.
            
        Returns:
            str: The path to the created file.
        """
        return self.file_handler.current_file 