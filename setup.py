#!/usr/bin/env python3
"""
Instagram Username Auto Claimer - Quick Setup Script
Made by Later.lol (c) 2025
"""

import os
import sys
import subprocess
import platform

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def setup_usernames():
    """Help user setup usernames.txt"""
    print("\n📝 Setting up usernames to check...")
    
    if os.path.exists('usernames.txt'):
        with open('usernames.txt', 'r') as f:
            content = f.read()
        
        # Check if user has added usernames
        active_usernames = [line.strip() for line in content.split('\n') 
                           if line.strip() and not line.strip().startswith('#')]
        
        if active_usernames:
            print(f"✅ Found {len(active_usernames)} usernames configured:")
            for username in active_usernames[:5]:  # Show first 5
                print(f"   - {username}")
            if len(active_usernames) > 5:
                print(f"   ... and {len(active_usernames) - 5} more")
            return True
    
    print("⚠️  No usernames configured yet.")
    print("📝 Please edit 'usernames.txt' and add usernames to check")
    print("   Remove the # from the lines to activate them")
    
    # Ask if user wants to add some now
    try:
        response = input("\nWould you like to add some usernames now? (y/n): ").lower()
        if response.startswith('y'):
            usernames = []
            print("Enter usernames to check (press Enter on empty line to finish):")
            while True:
                username = input("Username: ").strip()
                if not username:
                    break
                if username.isalnum() or '_' in username or '.' in username:
                    usernames.append(username)
                    print(f"✅ Added: {username}")
                else:
                    print("❌ Invalid username format")
            
            if usernames:
                # Append to usernames.txt
                with open('usernames.txt', 'a') as f:
                    f.write(f"\n# Added by setup script\n")
                    for username in usernames:
                        f.write(f"{username}\n")
                print(f"✅ Added {len(usernames)} usernames to usernames.txt")
                return True
    except KeyboardInterrupt:
        print("\n⚠️  Setup interrupted")
    
    return False

def setup_proxies():
    """Help user setup proxies.txt"""
    print("\n🌐 Proxy configuration...")
    
    try:
        response = input("Do you want to use proxies? (recommended) (y/n): ").lower()
        if not response.startswith('y'):
            print("⚠️  Running without proxies (may get rate limited)")
            return True
        
        print("📝 Please edit 'proxies.txt' and add your proxies")
        print("   Format: ip:port or ip:port:username:password")
        print("   You can find free proxies at:")
        print("   - https://www.freeproxylists.net/")
        print("   - https://www.proxy-list.download/")
        print("   - https://www.proxyscan.io/")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  Setup interrupted")
        return False

def main():
    """Main setup function"""
    print("🎯 Instagram Username Auto Claimer - Setup")
    print("Made by Later.lol (c) 2025")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        print(f"   Your version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Setup usernames
    if not setup_usernames():
        print("⚠️  You can add usernames later by editing usernames.txt")
    
    # Setup proxies
    setup_proxies()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit 'usernames.txt' to add usernames to check")
    print("2. (Optional) Edit 'proxies.txt' to add proxies")
    print("3. Run the checker:")
    
    if platform.system() == "Windows":
        print("   Windows: Double-click 'run.bat' or run 'python instagram_claimer.py'")
    else:
        print("   Linux: Run './run.sh' or 'python3 instagram_claimer.py'")
    
    print("\n📖 Read README.md for detailed instructions")
    print("📊 Check 'instagram_claimer.log' for detailed logs")
    print("💾 Available usernames will be saved to 'available_usernames.txt'")
    
    try:
        input("\nPress Enter to exit setup...")
    except KeyboardInterrupt:
        pass
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)