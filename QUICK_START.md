# 🚀 Quick Start Guide

## For Impatient Users 😅

### Windows Users
1. **Double-click `run.bat`** - It will auto-install everything!
2. **Edit `usernames.txt`** - Remove `#` from usernames you want to check
3. **Double-click `run.bat` again** - Start monitoring!

### Linux Users
1. **Run `./run.sh`** - It will auto-install everything!
2. **Edit `usernames.txt`** - Remove `#` from usernames you want to check  
3. **Run `./run.sh` again** - Start monitoring!

### Manual Setup (if needed)
```bash
# Install dependencies
pip install -r requirements.txt    # Windows
pip3 install -r requirements.txt   # Linux

# Run setup helper
python setup.py     # Windows
python3 setup.py    # Linux

# Start the checker
python instagram_claimer.py     # Windows
python3 instagram_claimer.py    # Linux
```

## Files You Need to Edit 📝

### `usernames.txt` (REQUIRED)
```
# Remove the # to activate usernames
coolgamer2025
awesomeuser
yourdesiredname
```

### `proxies.txt` (OPTIONAL but recommended)
```
# Format: ip:port or ip:port:user:pass
127.0.0.1:8080
192.168.1.1:3128:username:password
```

## What Happens When Running 🔄

1. ✅ Checks all your usernames every second
2. 🔔 Shows notification when username becomes available
3. 💾 Saves available usernames to `available_usernames.txt`
4. 📊 Logs everything to `instagram_claimer.log`

## Notifications 🔔

- **Windows**: Toast notifications in system tray
- **Linux**: Desktop notifications
- **Sound**: Optional beep (can disable in `config.json`)

## Tips for Success 💡

- **Use 5-10 usernames** to start
- **Add proxies** to avoid rate limits
- **Check shorter names** (3-8 chars) - they change hands more often
- **Run during weekends** - more account deletions
- **Be patient** - good usernames are rare!

## Need Help? 🆘

1. Check `instagram_claimer.log` for errors
2. Read the full `README.md`
3. Make sure you edited `usernames.txt` correctly
4. Try running without proxies first

---
**Made by Later.lol © 2025** | **Happy username hunting! 🎯**