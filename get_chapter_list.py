import requests
from bs4 import BeautifulSoup
import re
import argparse
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

def extract_chapter_number(chapter_str) :
    pattern = re.compile(r"[^A-Za-z\s]*[0-9]$")
    match = pattern.search(chapter_str)
    chapter = match.group(0) if match else "INVALID"
    return re.sub(r'[^0-9\.\,\;]','',chapter)

def get_series_link(title):
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

def get_chapter_list_by_name(title):
    # Cleans title to remove special characters (weebcentral search API doesn't like them)
    title = re.sub(r'[^a-zA-Z0-9\s]', ' ', title)

    # Collect manga link from title
    link = get_series_link(title)
    return get_chapter_list(link)

def get_chapter_list(link):
    series_id = re.findall(r'[A-Za-z0-9]{26}', link)[0]
    API = f"https://weebcentral.com/series/{series_id}/full-chapter-list"
    # print(f">>>  API: {API}")
    reponse = requests.get(API, headers=headers)
    soup = BeautifulSoup(reponse.text, "html.parser")

    chapter_list = []
    if reponse.status_code == 200:
        chapter_blocs_list = soup.select("div a")
        for i in range(len(chapter_blocs_list)):
            try:
                chapter_link = "https://weebcentral.com" + chapter_blocs_list[i]["href"]
                time = chapter_blocs_list[i].select_one("time").get_text(strip=True)
                chapter_number = chapter_blocs_list[i].select_one("span.grow span").get_text(strip=True)
                clean_chapter_number = extract_chapter_number(chapter_number.strip())

                # Add chapter to list
                chapter_list.append({"link": chapter_link, "chapter": clean_chapter_number, "time": time})

            except IndexError or KeyError:
                print(f"# Error: IndexError or KeyError \n# Chapter: {i}")

        return chapter_list

    else:
        print(f"# Error: Failed to fetch chapter number \n# Status code: {reponse.status_code}")
        return "Failed to fetch"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrap weebcentral series for chapter list (link, number, time)")
    parser.add_argument('-t', '--title', type=str, default=None, help="Manga title to search (e.g. 'Bleach')")
    parser.add_argument('-l', '--link', type=str, default=None, help="WeebCentral manga series URL (format: 'https://weebcentral.com/series/<26 random characters>/(optional)<title>')")
    args = parser.parse_args()

    if args.title:
        # print(f">>>  {get_last_chapter_by_name(args.title)}")
        print(json.dumps(get_chapter_list_by_name(args.title)))
    if args.link:
        # print(f">>>  {get_last_chapter(args.link)}")
        print(json.dumps(get_chapter_list(args.link)))
