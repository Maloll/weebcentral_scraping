<div align="center">

# 📚 WeebCentral Manga Scraper

**Un scraper Python simple, rapide et modulaire pour extraire les catalogues de mangas et suivre les derniers chapitres parus.**

[![Python Version](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![BeautifulSoup](https://img.shields.io/badge/Parser-BeautifulSoup4-00599C?style=flat-square)](https://www.crummy.com/software/BeautifulSoup/)
[![Requests](https://img.shields.io/badge/HTTP-Requests-orange?style=flat-square)](https://requests.readthedocs.io/)

```bash
pip install requests beautifulsoup4
```

<div align="left">

## 🚀 Utilisation

### 1. `get_last_chapter.py`

> Scrap weebcentral serie page for last manga chapter number & link

```bash
# Par titre
python get_last_chapter.py -t "Bleach"

# Par lien
python get_last_chapter.py -l "https://weebcentral.com/series/01J76XYYG1QRCBW24R5H3Y42R4/Bleach"
```

**Options :**

- `-t, --title TITLE` : Manga title to search (e.g. 'Bleach')
- `-l, --link LINK` : WeebCentral manga series URL

---

### 2. `get_manga_list_json.py`

> Collect mangas from WeebCentral into a JSON file

```bash
# Récupérer 2 pages (64 mangas) et enregistrer dans data.json
python get_manga_list_json.py -n 2 -s data
```

**Options :**

- `-n, --number NUMBER` : Number of pages to scrape (32 mangas per page)
- `-s, --save SAVE` : Output file name (saves to "\<name>.json" if provided)

---

## 🐍 Importation dans un script Python

Tu peux directement importer les fonctions dans un autre projet (ex: API FastAPI, script cron) :

```python
from scrap_utils import get_last_chapter_by_name

# Récupérer les infos du dernier chapitre
data = get_last_chapter_by_name("Chainsaw Man")

print(f"Dernier chapitre : {data['chapter']}")
print(f"Lire ici : {data['link']}")
```

---

## 📂 Structure du projet

| Fichier                  | Rôle                                                    |
| :----------------------- | :------------------------------------------------------ |
| `get_manga_list_json.py` | Scrape le catalogue complet et l'exporte en JSON        |
| `scrap_utils.py`         | Fonctions de recherche & extraction du dernier chapitre |
