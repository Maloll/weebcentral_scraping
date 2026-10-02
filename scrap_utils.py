import requests
from bs4 import BeautifulSoup
import re
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}
def get_link(title):
    api = f"https://weebcentral.com/search/data?display_mode=Full+Display&display_mode=Full%20Display&author=&text={title}&sort=Popularity&order=Descending&official=Any&anime=Any&adult=False&included_type=Manga"
    response = requests.get(api, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("article.bg-base-300")
    article = articles[0]
    title_tag = article.select_one("section a[href*='/series/']")
    return title_tag["href"]

def get_last_chapter(url):
    reponse = requests.get(url, headers=headers)
    if reponse.status_code == 200:
        soup = BeautifulSoup(reponse.text, "html.parser")
        last_chapter_link = "https://weebcentral.com" + soup.select("#chapter-list div a")[0]["href"]
        last_chapter = soup.select("#chapter-list div a span.grow span")[0].get_text(strip=True)
        last_chapter_clean = re.sub(r'[a-zA-Z]', '', last_chapter)
        return {"link": last_chapter_link, "chapter": last_chapter_clean}
    else:
        return -1

def get_last_chapter_by_name(title):
    link = get_link(title)
    return get_last_chapter(link)

# print(f"last chapter : {get_last_chapter("https://weebcentral.com/series/01J76XY7KWP8KX5RFGVZY5TR95/Shingeki-No-Kyojin")}")
# print(f"last chapter : {get_last_chapter_by_name('bleach')}")
