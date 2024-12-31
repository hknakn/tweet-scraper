# 🐦 Twitter Scraper

A modern, efficient Twitter scraper that collects tweets from any public profile. Built with Python and Selenium, featuring real-time progress tracking and beautiful console output.

## ✨ Features

- 🔄 Real-time tweet collection with live progress updates
- 💾 Immediate tweet saving (no waiting until the end)
- 🎯 Smart duplicate detection
- 📊 Comprehensive tweet metrics (comments, retweets, likes, views)
- 🌙 Headless mode support
- 🎨 Beautiful console interface with Rich
- 📁 Organized output in human-readable format

## 🎬 Demo

[Your demo video will go here]

## 🚀 Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/hknakn/tweet-scraper.git
   cd tweet-scraper
   ```

2. **Install dependencies**

   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up environment variables**

   ```bash
   cp .env.template .env
   ```

   Edit `.env` with your Twitter credentials:

   ```
   TWITTER_USERNAME=your_username_here
   TWITTER_PASSWORD=your_password_here
   ```

4. **Run the scraper**
   ```bash
   python3 scripts/get_tweets.py
   ```

## 📂 Project Structure

```
tweet-scraper/
├── src/
│   ├── browser/         # Browser management
│   ├── tweet/           # Tweet processing & file handling
│   └── config/          # Configuration settings
├── scripts/             # Executable scripts
├── data/
│   └── tweets/          # Saved tweet files
└── requirements.txt     # Project dependencies
```

## 📝 Output Format

Tweets are saved in a human-readable format:

```
📱 Tweets from @username
📅 Scraped on December 31, 2023 at 12:47 PM
────────────────────────────────────────────────────────────────

🕒 December 31, 2023 at 12:45 PM

This is an example tweet text...

💬 5 Comments  •  🔄 10 Retweets  •  ❤️ 20 Likes  •  👁️ 100 Views
────────────────────────────────────────────────────────────────
```

## ⚙️ Configuration

- **Headless Mode**: Run without visible browser window
- **User Agents**: Randomized for better scraping reliability
- **Scroll Settings**: Customizable scroll behavior
- **Output Directory**: Organized in `data/tweets/`

## 🛟 Support

If you encounter any issues or have questions, please open an issue on GitHub.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
