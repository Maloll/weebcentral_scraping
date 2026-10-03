<div align="center">

# 📚 WeebCentral Manga Scraper

**A simple, fast, and modular Python scraper to extract manga catalogs and track the latest released chapters.**

[![Python Version](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![BeautifulSoup](https://img.shields.io/badge/Parser-BeautifulSoup4-00599C?style=flat-square)](https://www.crummy.com/software/BeautifulSoup/)
[![Requests](https://img.shields.io/badge/HTTP-Requests-orange?style=flat-square)](https://requests.readthedocs.io/)

```bash
pip install requests beautifulsoup4
```

<div align="left">

## 🚀 Usage

### 1. `get_last_chapter.py`

> Scrape WeebCentral series page for the latest manga chapter number & link

```bash
# By title
python get_last_chapter.py -t "Bleach"

# By link
python get_last_chapter.py -l "[https://weebcentral.com/series/01J76XYYG1QRCBW24R5H3Y42R4/Bleach](https://weebcentral.com/series/01J76XYYG1QRCBW24R5H3Y42R4/Bleach)"
```

**Options:**

- `-t, --title TITLE` : Manga title to search (e.g. 'Bleach')
- `-l, --link LINK` : WeebCentral manga series URL

---

### 2. `get_manga_list_json.py`

> Collect mangas from WeebCentral into a JSON file

```bash
# Fetch 2 pages (64 mangas) and save to data.json
python get_manga_list_json.py -n 2 -s data
```

**Options:**

- `-n, --number NUMBER` : Number of pages to scrape (32 mangas per page)
- `-s, --save SAVE` : Output file name (saves to "\<name>.json" if provided)

---

## 🐍 Importing into a Python Script

You can directly import the functions into another project:

```python
from scrap_utils import get_last_chapter_by_name

# Fetch latest chapter info
data = get_last_chapter_by_name("Chainsaw Man")

print(f"Latest chapter: {data['chapter']}")
print(f"Read here: {data['link']}")
```

---

## 📂 Project Structure

| File                     | Role                                                 |
| :----------------------- | :--------------------------------------------------- |
| `get_manga_list_json.py` | Scrapes the full catalog and exports it to JSON      |
| `scrap_utils.py`         | Search & extraction functions for the latest chapter |

Made by [Maloll](https://discord.com/users/970348301448806430) ❤️
