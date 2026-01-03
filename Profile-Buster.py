import os
import sys
import time
import random
import subprocess
import urllib.parse  # Google Search URL banane ke liye
from datetime import datetime

# ==========================================
# 1. AUTO-INSTALLER (LIGHTWEIGHT ENGINE)
# ==========================================
def install_requirements():
    required_libs = ["requests", "beautifulsoup4", "colorama"]
    for lib in required_libs:
        try:
            __import__(lib if lib != "beautifulsoup4" else "bs4")
        except ImportError:
            print(f"[SYSTEM] Installing engine component: {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

install_requirements()

try:
    import requests
    from bs4 import BeautifulSoup
    from colorama import init, Fore, Style
    init(autoreset=True)
except Exception:
    pass

# ==========================================
# CONFIGURATION
# ==========================================
TOOL_NAME = "AUTONOMOUS-BOT V6 (Smart-AI)"
DEV_NAME = "🌸 vishal ❤️ subhi 🌸"
FILE_NAME = "profile.txt"

# Real User Agents (Phone & PC Mix)
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
]

# ==========================================
# 2. INTELLIGENT ENGINE
# ==========================================
class SmartBot:
    def log(self, msg, status="INFO"):
        t = datetime.now().strftime("%H:%M:%S")
        if status == "ERROR":
            print(Fore.RED + f"[{t}] {msg}")
        elif status == "SUCCESS":
            print(Fore.GREEN + f"[{t}] {msg}")
        else:
            print(Fore.CYAN + f"[{t}] {msg}")

    def get_headers(self):
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://www.google.com/"
        }

    def visit(self, url, is_search=False):
        """Universal Visitor (Link Visit or Google Search)"""
        headers = self.get_headers()
        try:
            if is_search:
                self.log(f"🔍 Searching Google: {url.replace('https://www.google.com/search?q=', '')[:30]}...", "INFO")
            else:
                self.log(f"🌐 Visiting Link: {url[:40]}...", "INFO")

            # REQUEST SEND KARNA
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string.strip() if soup.title else "No Title Found"
                
                # Agar Google Search hai, to result count dikhao
                if "Google" in title:
                    self.log(f"  > Google Accessed. Title: {title[:30]}", "SUCCESS")
                else:
                    self.log(f"  > Connected. Page Title: {title[:30]}...", "SUCCESS")
                
                # Human Waiting Simulation
                wait = random.uniform(2, 5)
                time.sleep(wait)
                return True
            else:
                self.log(f"  > Server Rejected (Status: {response.status_code})", "ERROR")
                return False

        except Exception as e:
            self.log(f"  > Connection Failed: {str(e)[:50]}", "ERROR")
            return False

    def process_line(self, line):
        """Smart Logic to decide what to do with the line"""
        line = line.strip()
        
        # 1. SKIP METADATA (Headers like [info], Name:, Email:)
        if line.startswith("[") or line.startswith("Name:") or line.startswith("Email:") or line.startswith("Dev"):
            # Chupchap skip karo, user ko disturb mat karo
            return 
            
        # 2. HANDLE URLS (Direct Links)
        if line.startswith("http://") or line.startswith("https://") or line.startswith("www."):
            if line.startswith("www."): line = "https://" + line
            self.visit(line, is_search=False)
            
        # 3. HANDLE KEYWORDS (Text -> Google Search)
        else:
            # Ye keyword hai, iska Google Search Link banao
            safe_query = urllib.parse.quote(line)
            search_url = f"https://www.google.com/search?q={safe_query}"
            self.visit(search_url, is_search=True)

# ==========================================
# 3. MAIN LOOP
# ==========================================
def run_smart_system():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + Style.BRIGHT + "="*50)
    print(Fore.GREEN + Style.BRIGHT + f"   {TOOL_NAME}")
    print(Fore.GREEN + f"   Dev    : {DEV_NAME}")
    print(Fore.GREEN + f"   Logic  : URL Visit + Auto Google Search")
    print(Fore.GREEN + Style.BRIGHT + "="*50 + "\n")

    bot = SmartBot()
    
    # Check File
    if not os.path.exists(FILE_NAME):
        bot.log("Creating profile.txt...", "INFO")
        with open(FILE_NAME, "w") as f:
            f.write("[keywords]\npython hacking\n[links]\nhttps://github.com")

    cycle = 0
    while True:
        cycle += 1
        print(Fore.YELLOW + f"\n--- [ CYCLE {cycle} STARTED ] ---")
        
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
        except:
            lines = []
        
        if not lines:
            bot.log("Profile.txt empty. Waiting...", "ERROR")
            time.sleep(10)
            continue
            
        random.shuffle(lines)
        
        for line in lines:
            bot.process_line(line)
            
        bot.log(f"Cycle {cycle} Finished. Cooling down...", "INFO")
        time.sleep(3)

if __name__ == "__main__":
    try:
        run_smart_system()
    except KeyboardInterrupt:
        print("\nStopped.")
