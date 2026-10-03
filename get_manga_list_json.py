import requests
import json
import argparse
from bs4 import BeautifulSoup

# HTTP headers mimicking a standard desktop web browser
# Essential to prevent WeebCentral from returning 403 Forbidden or bot challenge pages
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# Get a manga list from weebcentral
def get_manga_json(number_of_pages=10, save=True, file_name="data"):
    if number_of_pages < 1:
        number_of_pages = 1
        print("Error: Number of pages must be greater than 0")

    results = []

    for i in range(0, number_of_pages):
        # WeebCentral paginates with limit=32 and an offset multiplier (0, 32, 64, etc.)
        offset = i * 32
        api = (
            f"https://weebcentral.com/search/data?limit=32&offset={offset}"
            f"&display_mode=Full+Display&sort=Popularity&order=Descending"
            f"&official=Any&anime=Any&adult=False&included_type=Manga"
        )

        # 1. Fetch server-rendered HTML fragment
        response = requests.get(api, headers=headers)
        if response.status_code != 200:
            print(f"Warning: Failed to fetch page {i+1} (Status code: {response.status_code})")
            continue

        # 2. Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article.bg-base-300")

        # 3. Extract metadata from each manga card
        for article in articles:
            title_tag = article.select_one("section a[href*='/series/']")
            author_tag = article.select_one("a[href*='/search?author=']")
            datas = article.select("section div.opacity-70 span")
            clean_datas = [data.get_text(strip=True).replace(",", "") for data in datas]

            # Store everything in results[]
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
        # 4. Save the results to a .json file
        with open(f"{file_name}.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"> Saved {len(results)} mangas in {file_name}.json")

    return results

if __name__ == "__main__":
    # Command-Line Interface (CLI) configuration
    parser = argparse.ArgumentParser(description="Collect mangas from WeebCentral into a JSON file")
    parser.add_argument('-n', '--number', type=int, default=10, help="Number of pages to scrape (32 mangas per page)")
    parser.add_argument('-s', '--save', type=str, default=None, help="Output file name (saves to <name>.json if provided)")

    args = parser.parse_args()
    save_flag = True if args.save is not None else False

    get_manga_json(number_of_pages=args.number, save=save_flag, file_name=args.save)
