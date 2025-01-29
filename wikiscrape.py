from webbrowser import Mozilla
import requests
from bs4 import BeautifulSoup
import time
from colorama import init, Fore, Style

# Initialize colorama
init()

# URL of the page to scrape
url = "https://en.wikipedia.org/wiki/Firearm"

# user agent to prevent block requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}
response = requests.get(url, headers=headers)
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

soup = fetch_parse(url)

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
