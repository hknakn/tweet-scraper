# Twitter Scraper

A Python tool for scraping tweets from Twitter profiles. This tool uses Selenium to automate browser interactions and scrape tweets, including text content and engagement metrics (comments, retweets, likes, and views).

## Project Structure

```
twitter_scraper/
├── src/                      # Source code package
│   ├── browser/             # Browser management
│   │   └── browser_manager.py
│   ├── tweet/               # Tweet processing
│   │   ├── processor.py
│   │   └── file_handler.py
│   ├── config/              # Configuration
│   │   └── settings.py
│   └── scraper.py           # Main scraper class
├── scripts/                  # Command-line scripts
│   └── get_tweets.py        # Main script
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── .env                    # Twitter credentials
└── .env.template          # Template for .env file
```

## Features

- Scrapes tweets from any public Twitter profile
- Captures tweet text, timestamp, and engagement metrics
- Saves tweets immediately as they are found
- Handles rate limiting and scrolling automatically
- Supports headless mode for background operation
- Formats numbers in a human-readable way (e.g., 1.5K, 2.3M)
- Deduplicates tweets to avoid duplicates
- Provides progress bar and detailed logging

## Requirements

- Python 3.6+
- Chrome browser
- ChromeDriver (compatible with your Chrome version)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/twitter_scraper.git
   cd twitter_scraper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Twitter credentials:
   ```bash
   cp .env.template .env
   # Edit .env with your Twitter username and password
   ```

## Usage

Run the script:
```bash
python scripts/get_tweets.py
```

The script will:
1. Prompt for Twitter credentials if not found in `.env`
2. Ask for the username to scrape
3. Ask whether to run in headless mode
4. Start scraping tweets
5. Save tweets to a file with timestamp in the name

## Output Format

Tweets are saved in a text file with the following format:
```
📱 Tweets from @username
💾 Started scraping at YYYY-MM-DD HH:MM:SS
==========================================

🕒 January 01, 2024 at 12:34 PM

Tweet text goes here...

💬 123 Comments  |  🔄 45 Retweets  |  ❤️ 6.7K Likes  |  👁️ 89.1K Views
─────────────────────────────────────
```

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 