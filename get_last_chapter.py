import requests
from bs4 import BeautifulSoup
import re
import argparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# Get manga link from title, by using the weebcentral search api
def get_link(title):
    api = (
        f"https://weebcentral.com/search/data?display_mode=Full+Display"
        f"&display_mode=Full%20Display&author=&text={title}"
        f"&sort=Popularity&order=Descending&official=Any&anime=Any&adult=False"
    )

    response = requests.get(api, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article.bg-base-300")
        try:
            article = articles[0] # Get the first article from search results
            title_tag = article.select_one("section a[href*='/series/']")
            return title_tag["href"]
        except IndexError:
            return None
    else:
        return None

# Get last chapter from manga link
def get_last_chapter(link):

    # Check if link exists and is valid
    if link and link != None and link != "" and link != "None":
        link_valid = re.match(r'https://weebcentral.com/series/[A-Z0-9]{26}/.*', link)
        if not link_valid:
            print(f"# Error: Invalid link \n# Link must be in the format 'https://weebcentral.com/series/<26 random characters>/(optional <title>).'")
            return None
    else:
        print(f"# Error: Invalid link \n# Link must be in the format 'https://weebcentral.com/series/<26 random characters>/(optional <title>).'")
        return None
    reponse = requests.get(link, headers=headers)
    if reponse.status_code == 200:
        try:
            soup = BeautifulSoup(reponse.text, "html.parser")
            last_chapter_link = "https://weebcentral.com" + soup.select("#chapter-list div a")[0]["href"]
            last_chapter = soup.select("#chapter-list div a span.grow span")[0].get_text(strip=True)

            # Remove letters from chapter number
            last_chapter_clean = re.sub(r'[a-zA-Z]','',last_chapter).strip()

            # Return chapter number and link
            return {"link": last_chapter_link, "chapter": last_chapter_clean}
        except IndexError:
            print(f"# Error: Failed to fetch chapter number \n# Link: invalid or no chapter found")
            return None
    else:
        print(f"# Error: Failed to fetch chapter number \n# Status code: {reponse.status_code}")
        return None

# Get last chapter from manga title
def get_last_chapter_by_name(title):
    # Cleans title to remove special characters (weebcentral search API doesn't like them)
    title = re.sub(r'[^a-zA-Z0-9\s]', ' ', title)

    # Collect manga link from title
    link = get_link(title)
    return get_last_chapter(link)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrap weebcentral serie page for last manga chapter number & link")
    parser.add_argument('-t', '--title', type=str, default=None, help="Manga title to search (e.g. 'Bleach')")
    parser.add_argument('-l', '--link', type=str, default=None, help="WeebCentral manga series URL (format: 'https://weebcentral.com/series/<26 random characters>/(optional)<title>')")
    args = parser.parse_args()

    if args.title:
        print(f">>>  {get_last_chapter_by_name(args.title)}")

    if args.link:
        print(f">>>  {get_last_chapter(args.link)}")
