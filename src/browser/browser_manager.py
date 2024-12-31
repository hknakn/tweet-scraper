"""Browser management module for Twitter scraping."""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from rich.console import Console

from ..config.settings import USER_AGENTS, CHROME_OPTIONS, SCROLL_SETTINGS

# Initialize Rich console
console = Console()

class BrowserManager:
    """Manages browser operations for Twitter scraping."""
    
    def __init__(self, headless=False):
        """Initialize the browser manager.
        
        Args:
            headless (bool): Whether to run the browser in headless mode.
        """
        self.headless = headless
        self.driver = None
        self.wait = None
        self.setup_driver()

    def setup_driver(self):
        """Set up Chrome driver with optimized options."""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Add performance optimizations
        for option in CHROME_OPTIONS:
            chrome_options.add_argument(option)
        
        # Add random user agent
        chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
        
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def smart_scroll(self):
        """Optimized scroll with better performance.
        
        Returns:
            bool: True if the scroll was successful, False otherwise.
        """
        try:
            # Get initial metrics
            previous_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            current_position = self.driver.execute_script("return window.pageYOffset")
            
            # Calculate scroll amount
            scroll_amount = int(viewport_height * SCROLL_SETTINGS['scroll_increment'])
            
            # Scroll in smaller increments
            steps = SCROLL_SETTINGS['scroll_steps']
            for _ in range(steps):
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount/steps});")
                self.random_sleep(SCROLL_SETTINGS['min_scroll_wait'], SCROLL_SETTINGS['max_scroll_wait'])
            
            # Wait for content to load
            self.random_sleep(*SCROLL_SETTINGS['content_load_wait'])
            
            # Check if we actually moved and if new content loaded
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            new_position = self.driver.execute_script("return window.pageYOffset")
            
            # Return True if either we moved down or the page grew
            return new_position > current_position or new_height > previous_height
        except Exception as e:
            console.print(f"[red]Scroll error: {str(e)}[/red]")
            return False

    def random_sleep(self, min_seconds=0.5, max_seconds=2):
        """Sleep for a random amount of time to mimic human behavior.
        
        Args:
            min_seconds (float): Minimum sleep time in seconds.
            max_seconds (float): Maximum sleep time in seconds.
        """
        time.sleep(random.uniform(min_seconds, max_seconds))

    def login(self, username, password):
        """Login to Twitter with optimized waits.
        
        Args:
            username (str): Twitter username or email.
            password (str): Twitter password.
            
        Returns:
            bool: True if login was successful, False otherwise.
        """
        try:
            self.driver.get("https://twitter.com/i/flow/login")
            self.random_sleep(1, 2)

            # Enter username
            username_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
            )
            username_input.send_keys(username)
            username_input.send_keys(Keys.RETURN)
            self.random_sleep(0.5, 1)

            # Enter password
            password_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
            )
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)
            self.random_sleep(1, 2)

            # Verify login success
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Profile"]')))
                return True
            except:
                return False

        except Exception as e:
            console.print(f"[red]Login error: {str(e)}[/red]")
            return False

    def close(self):
        """Close the browser and clean up."""
        try:
            self.driver.quit()
        except:
            pass 