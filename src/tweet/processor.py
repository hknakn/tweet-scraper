"""Tweet processing module for Twitter scraping."""

import hashlib
from datetime import datetime
from selenium.webdriver.common.by import By
from rich.console import Console

# Initialize Rich console
console = Console()

class TweetProcessor:
    """Processes tweets extracted from Twitter."""
    
    def __init__(self):
        """Initialize the tweet processor."""
        self.processed_tweet_ids = set()

    def generate_tweet_id(self, tweet_text, timestamp):
        """Generate a unique ID for a tweet using text and timestamp.
        
        Args:
            tweet_text (str): The text content of the tweet.
            timestamp (str): The timestamp of the tweet.
            
        Returns:
            str: A unique hash ID for the tweet.
        """
        content = f"{tweet_text}{timestamp}".encode('utf-8')
        return hashlib.md5(content).hexdigest()

    def extract_text(self, tweet_element):
        """Extract text from a tweet element.
        
        Args:
            tweet_element: The Selenium element containing the tweet.
            
        Returns:
            str: The text content of the tweet.
        """
        try:
            text_element = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            return text_element.text.strip()
        except Exception as e:
            try:
                text_elements = tweet_element.find_elements(By.CSS_SELECTOR, '[lang]')
                for elem in text_elements:
                    if elem.text and len(elem.text.strip()) > 0:
                        return elem.text.strip()
            except:
                pass
        return ""

    def extract_timestamp(self, tweet_element):
        """Extract timestamp from a tweet element.
        
        Args:
            tweet_element: The Selenium element containing the tweet.
            
        Returns:
            str: The timestamp of the tweet.
        """
        try:
            time_element = tweet_element.find_element(By.TAG_NAME, "time")
            return time_element.get_attribute("datetime")
        except:
            return datetime.now().isoformat()

    def extract_metrics(self, tweet_element):
        """Extract engagement metrics from a tweet element.
        
        Args:
            tweet_element: The Selenium element containing the tweet.
            
        Returns:
            dict: A dictionary containing the tweet's metrics.
        """
        metrics = {
            'comments': '0',
            'retweets': '0',
            'likes': '0',
            'views': '0'
        }
        
        try:
            metric_groups = tweet_element.find_elements(By.CSS_SELECTOR, '[role="group"]')
            
            for group in metric_groups:
                try:
                    buttons = group.find_elements(By.CSS_SELECTOR, '[role="button"]')
                    for button in buttons:
                        aria_label = button.get_attribute('aria-label') or ''
                        aria_label = aria_label.lower()
                        
                        if 'repl' in aria_label:
                            metrics['comments'] = ''.join(filter(str.isdigit, aria_label))
                        elif 'repost' in aria_label or 'retweet' in aria_label:
                            metrics['retweets'] = ''.join(filter(str.isdigit, aria_label))
                        elif 'like' in aria_label:
                            metrics['likes'] = ''.join(filter(str.isdigit, aria_label))
                except:
                    continue
            
            try:
                analytics = tweet_element.find_element(By.CSS_SELECTOR, '[href*="analytics"]')
                aria_label = analytics.get_attribute('aria-label') or ''
                if 'view' in aria_label.lower():
                    metrics['views'] = ''.join(filter(str.isdigit, aria_label))
            except:
                pass
            
        except:
            pass
        
        return metrics

    def process_tweet(self, tweet_element):
        """Process a single tweet element and return structured data.
        
        Args:
            tweet_element: The Selenium element containing the tweet.
            
        Returns:
            dict: A dictionary containing the processed tweet data.
        """
        try:
            # Extract tweet text
            tweet_text = self.extract_text(tweet_element)
            if not tweet_text:
                return None
            
            # Extract timestamp
            timestamp = self.extract_timestamp(tweet_element)
            
            # Check for duplicates
            tweet_id = self.generate_tweet_id(tweet_text, timestamp)
            if tweet_id in self.processed_tweet_ids:
                return None
            
            self.processed_tweet_ids.add(tweet_id)
            
            # Extract metrics
            metrics = self.extract_metrics(tweet_element)
            
            tweet_data = {
                'text': tweet_text,
                'timestamp': timestamp,
                'metrics': metrics
            }
            
            return tweet_data
            
        except Exception as e:
            console.print(f"[red]Error processing tweet: {str(e)}[/red]")
            return None 