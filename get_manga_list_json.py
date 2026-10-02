import requests
import json
from bs4 import BeautifulSoup
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# Get a manga list from weebcentral
def get_manga_json(number_of_pages=10, save=True):
    if number_of_pages < 1:
        number_of_pages = 1
        print("Error: Number of pages must be greater than 0")

    results = []
    for i in range(0, number_of_pages):
        offset = i * 32
        api = f"https://weebcentral.com/search/data?limit=32&offset={offset}&display_mode=Full+Display&display_mode=Full+Display&sort=Popularity&order=Descending&official=Any&anime=Any&adult=False&included_type=Manga"

        # Get data from api
        response = requests.get(api, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article.bg-base-300")

        # Create a list of mangas from the articles
        for article in articles:
            title_tag = article.select_one("section a[href*='/series/']")
            author_tag = article.select_one("a[href*='/search?author=']")
            datas = article.select("section div.opacity-70 span")
            clean_datas = [data.get_text(strip=True).replace(",", "") for data in datas]
            if title_tag:
                results.append({
                    "title": title_tag.get_text(strip=True).replace("Official", ""),
                    "url": title_tag["href"],
                    "author": author_tag.get_text(strip=True),
                    "year": clean_datas[0],
                    "status": clean_datas[1],
                    "format": clean_datas[2],
                    "tags": clean_datas[3:],
                })
        print(f"Scraped {i+1} pages && {len(results)} mangas")

    if save:
        # Save the results to a .json file
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

    return results
