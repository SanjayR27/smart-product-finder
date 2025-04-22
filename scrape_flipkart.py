import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for search query (phones under ₹10,000)
url = "https://www.flipkart.com/search?q=phones+under+10000"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Send request to Flipkart
response = requests.get(url, headers=headers)

# Check the first 500 characters of the HTML response
print(response.text[:500])  # Prints the first 500 characters of the HTML response

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# List to store product data
products = []

# Parsing the product blocks
for item in soup.select("div._1AtVbE"):
    name = item.select_one("div._4rR01T")
    price = item.select_one("div._30jeq3")
    rating = item.select_one("div._3LWZlK")
    features = item.select_one("ul._1xgFaf")

    if name and price:
        product_data = {
            "name": name.text,
            "price": price.text.replace("₹", "").replace(",", ""),
            "rating": rating.text if rating else "N/A",
        }

        # Get camera, RAM, storage, battery
        if features:
            feature_list = [feature.text for feature in features.select("li")]
            for feature in feature_list:
                if "camera" in feature.lower():
                    product_data["camera"] = feature
                if "ram" in feature.lower():
                    product_data["ram"] = feature
                if "battery" in feature.lower():
                    product_data["battery"] = feature
                if "storage" in feature.lower():
                    product_data["storage"] = feature

        # Append data
        products.append(product_data)

# Convert to DataFrame and save to CSV
df = pd.DataFrame(products)
df.to_csv("data/flipkart_phones_detailed.csv", index=False)
print("✅ Data saved to data/flipkart_phones_detailed.csv")
