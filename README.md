# Instagram Username Auto Claimer & Checker 🎯

**Made by Later.lol © 2025**

A fast and reliable Instagram username checker that monitors desired usernames and instantly notifies you when they become available. Works on both Windows and Linux with proxy support for avoiding rate limits.

## Features ✨

- ⚡ **Real-time monitoring** - Checks usernames every second
- 🔔 **Instant notifications** - Windows toast notifications & Linux desktop notifications  
- 🌐 **Proxy support** - Rotate through multiple proxies to avoid rate limiting
- 🖥️ **Cross-platform** - Works on Windows, Linux, and other systems
- 📊 **Detailed logging** - Track all checks and available usernames
- ⚙️ **Configurable** - Customizable check intervals and settings
- 📝 **Auto-save** - Automatically saves available usernames with timestamps

## Installation 🚀

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Setup

1. **Clone or download this project**
2. **Install dependencies:**

**Windows:**
```cmd
pip install -r requirements.txt
```

**Linux:**
```bash
pip3 install -r requirements.txt
```

3. **Configure your usernames** (edit `usernames.txt`):
```
# Remove the # and add your desired usernames
coolgamer2025
awesomeuser
yourdesiredname
```

4. **Configure proxies** (optional, edit `proxies.txt`):
```
# Format: ip:port or ip:port:username:password
127.0.0.1:8080
192.168.1.1:3128:user:pass
```

## Usage 📖

### Basic Usage

**Windows:**
```cmd
python instagram_claimer.py
```

**Linux:**
```bash
python3 instagram_claimer.py
```

### Advanced Usage

**Check once and exit:**
```bash
python instagram_claimer.py --check-once
```

**Use custom config file:**
```bash
python instagram_claimer.py --config my_config.json
```

**List available usernames found:**
```bash
python instagram_claimer.py --list-available
```

### Configuration Options

Edit `config.json` to customize:

```json
{
    "check_interval": 1,          // Seconds between full checks
    "min_delay_seconds": 1,       // Minimum delay between requests
    "max_retries": 3,            // Max retries for failed requests
    "timeout": 10,               // Request timeout in seconds
    "notification_sound": true,   // Play sound with notifications
    "log_level": "INFO"          // Logging level (DEBUG, INFO, WARNING, ERROR)
}
```

## How It Works 🔍

1. **Loads usernames** from `usernames.txt`
2. **Loads proxies** from `proxies.txt` (optional)
3. **Checks each username** by making requests to Instagram
4. **Detects availability** by analyzing HTTP status codes and page content
5. **Sends notifications** when a username becomes available
6. **Logs everything** to `instagram_claimer.log` and console
7. **Saves results** to `available_usernames.txt`

## File Structure 📁

```
darkknight/
├── instagram_claimer.py      # Main script
├── config.json              # Configuration settings
├── usernames.txt            # List of usernames to check
├── proxies.txt              # List of proxies (optional)
├── requirements.txt         # Python dependencies
├── instagram_claimer.log    # Log file (auto-created)
├── available_usernames.txt  # Available usernames (auto-created)
└── README.md               # This file
```

## Notifications 🔔

### Windows
- Toast notifications appear in the system tray
- Optional system beep sound

### Linux
- Desktop notifications via `plyer`
- Optional system beep sound

### All Platforms
- Console alerts as fallback
- Logged to file for later review

## Proxy Support 🌐

### Supported Formats
- `ip:port` - Basic HTTP proxy
- `ip:port:username:password` - Authenticated proxy

### Benefits
- Avoid Instagram rate limiting
- Prevent IP blocking
- Faster checking with rotation
- Better success rates

### Free Proxy Sources
- https://www.freeproxylists.net/
- https://www.proxy-list.download/
- https://www.proxyscan.io/

## Tips for Success 💡

### Username Selection
- **Shorter usernames** (3-8 characters) become available more often
- **Common words + numbers** have higher turnover
- **Avoid offensive/trademarked** names
- **Check deleted/renamed** accounts

### Optimization
- Use **multiple proxies** for faster checking
- Start with **5-10 usernames** to test
- **Monitor logs** for any issues
- Run during **peak deletion times** (weekends)

### Rate Limiting
- Default settings are conservative
- Increase `check_interval` if getting blocked
- Use more proxies for faster checking
- Monitor `instagram_claimer.log` for errors

## Troubleshooting 🔧

### Common Issues

**"No usernames to check"**
- Edit `usernames.txt` and remove `#` from desired usernames

**Notifications not working**
- Windows: Ensure notifications are enabled in system settings
- Linux: Install notification daemon (`sudo apt-get install libnotify-bin`)

**Getting rate limited**
- Add more proxies to `proxies.txt`
- Increase `check_interval` in `config.json`
- Use authenticated proxies

**Proxy errors**
- Test proxies manually before adding
- Remove non-working proxies
- Consider paid proxy services

### Log Analysis
Check `instagram_claimer.log` for detailed information:
- Request errors and timeouts
- Proxy connection issues
- Username check results
- System notifications

## Legal Notice ⚖️

This tool is for educational purposes only. Users are responsible for:
- Complying with Instagram's Terms of Service
- Following local laws and regulations
- Using ethical practices
- Not engaging in spam or harassment

**Disclaimer:** This tool does not guarantee username acquisition. Instagram may implement additional anti-automation measures.

## License 📄

Copyright © 2025 Later.lol - All rights reserved.

## Support 💬

For issues, suggestions, or improvements, please check the logs first and ensure you're following the setup instructions correctly.

---

**Happy username hunting! 🎯**