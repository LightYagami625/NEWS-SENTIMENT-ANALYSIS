import requests
from bs4 import BeautifulSoup
import sys

# The URL of the news website we want to scrape
URL = "https://www.bbc.com/"

OUTPUT_FILE = "headlines.txt"

def fetch_headlines():

    response = requests.get(URL)
    response.raise_for_status()
    # print(response.status_code())
    soup = BeautifulSoup(response.text, 'html.parser')
    headline_tags = soup.find_all(['h2','p'])
        
    if not headline_tags:
        print("No headlines found. The website structure might have changed.")
        return []

    headlines = [tag.get_text() for tag in headline_tags]
        
    return headlines

def save_headlines(headlines):
    if not headlines:
        print("No headlines to save.")
        return
    count =1
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for line in headlines:
                count +=1
                f.write(f"{line}\n")
                # if count > 20:
                #     break
                
        
        print(f"Successfully saved {len(headlines)} headlines to {OUTPUT_FILE}")
        
    except IOError as e:
        print(f"Error writing to file {OUTPUT_FILE}: {e}")
        sys.exit(1)


scraped_headlines = fetch_headlines()
save_headlines(scraped_headlines)