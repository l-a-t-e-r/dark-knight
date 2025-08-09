#!/usr/bin/env python3
"""
Instagram Username Auto Claimer and Checker
Checks usernames every second and notifies when available
Supports proxy rotation and cross-platform notifications
"""

import requests
import time
import random
import json
import logging
import platform
import os
from datetime import datetime
from typing import List, Optional
import threading
from queue import Queue
import argparse

# Platform-specific imports for notifications
if platform.system() == "Windows":
    try:
        import win10toast
    except ImportError:
        print("Installing win10toast for Windows notifications...")
        os.system("pip install win10toast")
        import win10toast
elif platform.system() == "Linux":
    try:
        import plyer
    except ImportError:
        print("Installing plyer for Linux notifications...")
        os.system("pip install plyer")
        import plyer

class InstagramChecker:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.usernames = self.load_usernames()
        self.proxies = self.load_proxies()
        self.available_usernames = []
        self.session = requests.Session()
        self.running = True
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('instagram_claimer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Setup notification system
        self.setup_notifications()
        
        # Rate limiting
        self.request_queue = Queue()
        self.last_request_time = 0
        self.min_delay = self.config.get("min_delay_seconds", 1)
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config
            default_config = {
                "check_interval": 1,
                "min_delay_seconds": 1,
                "max_retries": 3,
                "timeout": 10,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "notification_sound": True,
                "log_level": "INFO"
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
    
    def load_usernames(self):
        """Load usernames from usernames.txt"""
        try:
            with open('usernames.txt', 'r') as f:
                usernames = [line.strip() for line in f if line.strip()]
            self.logger.info(f"Loaded {len(usernames)} usernames to check")
            return usernames
        except FileNotFoundError:
            self.logger.error("usernames.txt not found! Creating sample file...")
            with open('usernames.txt', 'w') as f:
                f.write("# Add usernames to check (one per line)\n")
                f.write("# Remove the # from the lines below and add your desired usernames\n")
                f.write("# example_username\n")
                f.write("# another_username\n")
            return []
    
    def load_proxies(self):
        """Load proxies from proxies.txt"""
        try:
            with open('proxies.txt', 'r') as f:
                proxies = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Support formats: ip:port or ip:port:username:password
                        parts = line.split(':')
                        if len(parts) >= 2:
                            if len(parts) == 2:
                                proxy = {
                                    'http': f'http://{parts[0]}:{parts[1]}',
                                    'https': f'http://{parts[0]}:{parts[1]}'
                                }
                            elif len(parts) == 4:
                                proxy = {
                                    'http': f'http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}',
                                    'https': f'http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}'
                                }
                            else:
                                continue
                            proxies.append(proxy)
            
            if proxies:
                self.logger.info(f"Loaded {len(proxies)} proxies")
            else:
                self.logger.info("No proxies loaded, using direct connection")
            return proxies
        except FileNotFoundError:
            self.logger.info("proxies.txt not found, using direct connection")
            with open('proxies.txt', 'w') as f:
                f.write("# Add proxies (one per line)\n")
                f.write("# Format: ip:port or ip:port:username:password\n")
                f.write("# Example:\n")
                f.write("# 127.0.0.1:8080\n")
                f.write("# 192.168.1.1:3128:user:pass\n")
            return []
    
    def setup_notifications(self):
        """Setup platform-specific notifications"""
        self.system = platform.system()
        if self.system == "Windows":
            self.toaster = win10toast.ToastNotifier()
        elif self.system == "Linux":
            pass  # plyer will be used directly
    
    def send_notification(self, username):
        """Send platform-specific notification"""
        title = "🎉 Instagram Username Available!"
        message = f"Username '{username}' is now available to claim!"
        
        try:
            if self.system == "Windows":
                self.toaster.show_toast(
                    title,
                    message,
                    duration=10,
                    icon_path=None,
                    threaded=True
                )
            elif self.system == "Linux":
                plyer.notification.notify(
                    title=title,
                    message=message,
                    timeout=10
                )
            else:
                # Fallback for other systems
                print(f"\n🚨 ALERT: {title} - {message}")
                
            # Also play system sound if configured
            if self.config.get("notification_sound", True):
                if self.system == "Windows":
                    os.system("echo \a")
                elif self.system == "Linux":
                    os.system("paplay /usr/share/sounds/alsa/Front_Left.wav 2>/dev/null || echo '\a'")
                    
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")
            print(f"\n🚨 ALERT: {title} - {message}")
    
    def get_random_proxy(self):
        """Get a random proxy from the list"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
    
    def check_username_availability(self, username):
        """Check if a username is available on Instagram"""
        url = f"https://www.instagram.com/{username}/"
        
        headers = {
            'User-Agent': self.config.get("user_agent"),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        proxy = self.get_random_proxy()
        
        try:
            # Rate limiting
            current_time = time.time()
            if current_time - self.last_request_time < self.min_delay:
                time.sleep(self.min_delay - (current_time - self.last_request_time))
            
            response = self.session.get(
                url,
                headers=headers,
                proxies=proxy,
                timeout=self.config.get("timeout", 10),
                allow_redirects=True
            )
            
            self.last_request_time = time.time()
            
            # Check response
            if response.status_code == 404:
                return True  # Username is available
            elif response.status_code == 200:
                # Check if it's the "User not found" page
                if "Sorry, this page isn't available" in response.text or "The link you followed may be broken" in response.text:
                    return True  # Username is available
                return False  # Username is taken
            else:
                self.logger.warning(f"Unexpected status code {response.status_code} for {username}")
                return None  # Unknown status
                
        except requests.exceptions.ProxyError:
            self.logger.warning(f"Proxy error for {username}, trying without proxy")
            return None
        except requests.exceptions.Timeout:
            self.logger.warning(f"Timeout checking {username}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error checking {username}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error checking {username}: {e}")
            return None
    
    def check_all_usernames(self):
        """Check all usernames in the list"""
        if not self.usernames:
            self.logger.warning("No usernames to check!")
            return
        
        self.logger.info(f"Checking {len(self.usernames)} usernames...")
        
        for username in self.usernames:
            if not self.running:
                break
                
            try:
                availability = self.check_username_availability(username)
                
                if availability is True:
                    if username not in self.available_usernames:
                        self.available_usernames.append(username)
                        self.logger.info(f"🎉 USERNAME AVAILABLE: {username}")
                        self.send_notification(username)
                        
                        # Save to available usernames file
                        with open('available_usernames.txt', 'a') as f:
                            f.write(f"{username} - Available at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                elif availability is False:
                    if username in self.available_usernames:
                        self.available_usernames.remove(username)
                    self.logger.debug(f"Username {username} is taken")
                
                else:
                    self.logger.debug(f"Could not check {username} (network/proxy issue)")
                
                # Small delay between checks to avoid rate limiting
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                self.logger.info("Interrupted by user")
                self.running = False
                break
            except Exception as e:
                self.logger.error(f"Error checking {username}: {e}")
                continue
    
    def run(self):
        """Main run loop"""
        self.logger.info("Starting Instagram Username Checker...")
        self.logger.info(f"Checking {len(self.usernames)} usernames every {self.config['check_interval']} seconds")
        self.logger.info("Press Ctrl+C to stop")
        
        if not self.usernames:
            self.logger.error("No usernames to check! Please add usernames to usernames.txt")
            return
        
        try:
            while self.running:
                start_time = time.time()
                self.check_all_usernames()
                
                # Calculate sleep time
                elapsed = time.time() - start_time
                sleep_time = max(0, self.config["check_interval"] - elapsed)
                
                if sleep_time > 0 and self.running:
                    self.logger.debug(f"Waiting {sleep_time:.2f} seconds before next check...")
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            self.logger.info("Stopping checker...")
            self.running = False
        except Exception as e:
            self.logger.error(f"Unexpected error in main loop: {e}")
        finally:
            self.logger.info("Instagram Username Checker stopped")

def main():
    parser = argparse.ArgumentParser(description='Instagram Username Auto Claimer and Checker')
    parser.add_argument('--config', default='config.json', help='Configuration file path')
    parser.add_argument('--check-once', action='store_true', help='Check once and exit')
    parser.add_argument('--list-available', action='store_true', help='List currently available usernames and exit')
    
    args = parser.parse_args()
    
    checker = InstagramChecker(args.config)
    
    if args.list_available:
        if os.path.exists('available_usernames.txt'):
            with open('available_usernames.txt', 'r') as f:
                print(f.read())
        else:
            print("No available usernames found yet.")
        return
    
    if args.check_once:
        checker.check_all_usernames()
    else:
        checker.run()

if __name__ == "__main__":
    main()