from webbrowser import Mozilla
import requests
from bs4 import BeautifulSoup
import time
from colorama import init, Fore, Style

# Initialize colorama
init()
print(f"{Fore.RED}V1.0.1\n{Style.RESET_ALL}")
print(f"{Fore.BLUE}Developed by{Style.RESET_ALL}{Fore.RED}  Wheatly{Style.RESET_ALL}\n")

print(f"{Fore.CYAN}Welcome to WikiScraper! This program will scrape the main headings and subheadings of most standard wikipedia pages.{Style.RESET_ALL}")

def is_valid_url(url):
    try:
        # Check if URL has https:// only once
        if url.count('https://') > 1 or url.count('http://') > 1:
            return False
        return url.startswith(('http://', 'https://')) and ' ' not in url
    except:
        return False

# URL of the page to scrape
while True:
    user_url = input(f"{Fore.RED}Please do not scrape random websites.{Style.RESET_ALL}\nMake sure you have permission from the site first.\nEnter the URL of the page you want to scrape: ").strip()
    
    if is_valid_url(user_url):
        break
    else:
        print("Please enter a valid URL starting with http:// or https://")

# user agent to prevent block requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}
response = requests.get(user_url, headers=headers)
def fetch_parse(url, delay=2):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to load page: {response.status_code}")
        soup = BeautifulSoup(response.content, 'html.parser')
        time.sleep(delay)
        return soup
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        return None

soup = fetch_parse(user_url)

if soup:
    print(f"{Fore.GREEN}Soup fetched successfully{Style.RESET_ALL}")
    
    content_div = soup.find(id="mw-content-text")
    if content_div:

        main_headings = content_div.find_all('h2')
        
        for h2 in main_headings:
            # Print main heading
            h2_text = h2.text.strip()
            print(f"\n{Fore.GREEN}-{h2_text}{Style.RESET_ALL}")
            
            # Find first h3 after this h2
            next_h3 = h2.find_next('h3')
            if next_h3 and next_h3.find_previous('h2') == h2:
                h3_text = next_h3.text.strip()
                print(f"{Fore.CYAN}   └─ {h3_text}{Style.RESET_ALL}")
                while next_h3 and next_h3.find_previous('h2') == h2:
                    next_h3 = next_h3.find_next('h3')
                    if next_h3 and next_h3.find_previous('h2') == h2:
                        h3_text = next_h3.text.strip()
                        print(f"{Fore.CYAN}   └─ {h3_text}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Content div not found{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}Failed to fetch and parse URL{Style.RESET_ALL}")
