import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

START_URL = "https://books.toscrape.com/"
TARGET_COUNT = 20
OUTPUT_CSV = "books.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BookScraper/1.0)"
}

def parse_books_from_page(soup):
    """Return list of dicts with title, price, rating from a page soup."""
    items = []
    cards = soup.find_all("article", class_="product_pod")
    for card in cards:
        # title is in the <a title="...">
        a = card.h3.find("a")
        title = a.get("title", "").strip() if a else "Unknown"

        # price
        price_tag = card.find("p", class_="price_color")
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        # rating is encoded as a class on <p class="star-rating X">
        rating_tag = card.find("p", class_="star-rating")
        rating = "Unknown"
        if rating_tag and rating_tag.has_attr("class") and len(rating_tag["class"]) > 1:
            rating = f"{rating_tag['class'][1]} stars"

        items.append({"title": title, "price": price, "rating": rating})
    return items

def find_next_url(soup, current_url):
    """Return absolute URL for the 'next' page, or None if none exists."""
    pager = soup.find("li", class_="next")
    if not pager:
        return None
    a = pager.find("a")
    if not a or not a.get("href"):
        return None
    return urljoin(current_url, a["href"])

def fetch_soup(url):
    """GET a page and return BeautifulSoup parsed HTML."""
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def save_to_csv(rows, filename=OUTPUT_CSV):
    fieldnames = ["title", "price", "rating"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n📁 Saved {len(rows)} books to '{filename}'")

def main():
    url = START_URL
    collected = []

    while url and len(collected) < TARGET_COUNT:
        soup = fetch_soup(url)
        page_items = parse_books_from_page(soup)

        # take only what we still need to hit TARGET_COUNT
        needed = TARGET_COUNT - len(collected)
        collected.extend(page_items[:needed])

        print(f"Scraped {len(collected)} / {TARGET_COUNT} so far (from: {url})")

        if len(collected) >= TARGET_COUNT:
            break

        url = find_next_url(soup, url)

    # print nicely
    for i, b in enumerate(collected, start=1):
        print(f"{i:>2}. {b['title']} — {b['price']} — {b['rating']}")

    # save to CSV
    save_to_csv(collected, OUTPUT_CSV)

if __name__ == "__main__":
    main()
