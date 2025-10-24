# Python Web Scraper — BooksToScrape Demo

A lightweight Python scraper that collects book data from [BooksToScrape.com](https://books.toscrape.com/).  
The script extracts **titles**, **prices**, and **ratings**, then stores everything neatly in a CSV file.

---

## 🚀 Features
- Scrapes multiple pages automatically (pagination support)
- Extracts structured data: `title`, `price`, and `rating`
- Saves output to `books.csv` for easy viewing
- Built with `requests` and `BeautifulSoup` — no external API required
- Fast and simple to customize for other sites

---

## 🧠 Tech Stack
- **Python 3.9+**
- **Libraries:** `requests`, `beautifulsoup4`, `csv`, `urllib.parse`

---

## 📦 Requirements
Install dependencies:
```bash
pip install requests beautifulsoup4
