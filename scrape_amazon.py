import requests
from bs4 import BeautifulSoup
import pandas as pd
import random


def scrape_amazon(search_term, max_results=10):
    headers_list = [
        {"User-Agent": "Mozilla/5.0"},
        {"User-Agent": "Chrome/90.0"},
        {"User-Agent": "Safari/537.36"}
    ]

    search_url = f"https://www.amazon.in/s?k={search_term.replace(' ', '+')}"
    res = requests.get(search_url, headers=random.choice(headers_list))
    soup = BeautifulSoup(res.content, 'html.parser')

    products = []
    items = soup.select("div.s-result-item[data-component-type='s-search-result']")

    for item in items:
        name = item.select_one("h2 a span")
        price = item.select_one("span.a-price-whole")
        rating = item.select_one("span.a-icon-alt")

        if name and price:
            rating_val = None
            if rating:
                try:
                    rating_val = float(rating.text.split(" ")[0])
                except:
                    rating_val = None

            products.append({
                "product_name": name.text.strip(),
                "price": int(price.text.replace(",", "").strip()),
                "rating": rating_val
            })

        if len(products) >= max_results:
            break

    return pd.DataFrame(products)


# 🔁 Example Usage
if __name__ == "__main__":
    df = scrape_amazon("phones under 10000", max_results=15)
    df.to_csv("amazon_products.csv", index=False)
    print("✅ Scraped and saved to amazon_products.csv")
