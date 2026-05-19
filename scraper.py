import time
import pandas as pd
from playwright.sync_api import sync_playwright

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
CATEGORY_URLS = [
    "https://kathmandupost.com/politics",
    "https://kathmandupost.com/money",
    "https://kathmandupost.com/national",
]
PAGES_PER_CATEGORY = 3
CSV_FILE = "nepal_news.csv"


# ─────────────────────────────────────────────
# Collect article URLs from category pages
# ─────────────────────────────────────────────
def get_article_urls(page, category_url, pages=3):
    urls = []
    for p in range(1, pages + 1):
        try:
            url = f"{category_url}?page={p}"
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(2000)

            links = page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
            for href in links:
                if href and href.startswith("/"):
                    parts = href.strip("/").split("/")
                    # Only keep dated article URLs like /national/2026/05/13/article-slug
                    if len(parts) >= 4 and parts[1].isdigit():
                        full_url = "https://kathmandupost.com" + href
                        urls.append(full_url)

            print(f"  Page {p}: {len(set(urls))} URLs so far...")

        except Exception as e:
            print(f"  Error on page {p}: {e}")

    return list(set(urls))


# ─────────────────────────────────────────────
# Scrape a single article
# ─────────────────────────────────────────────
def scrape_article(page, url):
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(2000)

        # Title from <title> tag
        title = page.title().replace(" - The Kathmandu Post", "").strip()

        # Date — look for "Published at" text anywhere on page
        date = ""
        try:
            date_el = page.locator("text=Published at").first
            date = date_el.inner_text().replace("Published at :", "").replace("Published at:", "").strip()
            date = date.split("Updated")[0].strip()
        except:
            pass

        # Category from URL
        parts = url.replace("https://kathmandupost.com/", "").split("/")
        category = parts[0] if parts else "general"

        # All paragraph text on page
        paragraphs = page.eval_on_selector_all("p", "els => els.map(e => e.innerText.trim()).filter(t => t.length > 30)")
        content = " ".join(paragraphs)

        if not title or len(content) < 200:
            print(f"    ⚠ Skipped (content_len={len(content)})")
            return None

        return {
            "title": title,
            "date": date,
            "category": category,
            "content": content,
            "url": url,
        }

    except Exception as e:
        print(f"  Failed: {e}")
        return None


# ─────────────────────────────────────────────
# Main scraping pipeline
# ─────────────────────────────────────────────
def run_scraper():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        print("\n🔍 Collecting article URLs...")
        all_urls = []
        for cat_url in CATEGORY_URLS:
            print(f"\nCategory: {cat_url}")
            urls = get_article_urls(page, cat_url, pages=PAGES_PER_CATEGORY)
            all_urls += urls

        all_urls = list(set(all_urls))
        print(f"\n📄 Total unique URLs: {len(all_urls)}")

        print("\n🌐 Scraping articles...")
        articles = []
        for i, url in enumerate(all_urls):
            print(f"  [{i+1}/{len(all_urls)}] {url}")
            article = scrape_article(page, url)
            if article:
                articles.append(article)
            time.sleep(0.5)

        browser.close()

    df = pd.DataFrame(articles)
    df.drop_duplicates(subset="url", inplace=True)
    df.to_csv(CSV_FILE, index=False)
    print(f"\n✅ Saved {len(df)} articles to {CSV_FILE}\n")


if __name__ == "__main__":
    run_scraper()