"""Configuration settings for the Twitter scraper."""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

CHROME_OPTIONS = [
    "--start-maximized",
    "--disable-notifications",
    "--disable-popup-blocking",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-infobars"
]

SCROLL_SETTINGS = {
    'max_retries': 3,
    'scroll_increment': 0.75,  # 75% of viewport
    'scroll_steps': 3,
    'min_scroll_wait': 0.3,
    'max_scroll_wait': 0.5,
    'content_load_wait': (1, 1.5)
}

FILE_SETTINGS = {
    'timestamp_format': '%Y%m%d_%H%M%S',
    'date_format': '%B %d, %Y at %I:%M %p',
    'separator_line': "=" * 100,
    'subseparator_line': "─" * 100
} 