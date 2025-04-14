import requests
from bs4 import BeautifulSoup
import json
from crawler.utils import safe_request
# Define the URLs
MARKET_PRODUCTLINK = [
    "https://agriculture.ec.europa.eu/data-and-analysis/markets/overviews/market-observatories_en", 
    "https://agriculture.ec.europa.eu/farming/animal-products_en",
    "https://agriculture.ec.europa.eu/farming/crop-productions-and-plant-based-products_en"
]

class_name = "ecl-link ecl-link--standalone"

final_data = []

for product_link in MARKET_PRODUCTLINK:
    response = safe_request(product_link)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', class_=class_name)
    for link in links:
        href = link.get('href')
        if href and href.startswith("/"):  
            final_data.append(href)

    final_data = final_data[:-2]


final_data = ["https://agriculture.ec.europa.eu" + data for data in final_data]


with open("product_links.json", "w") as f:
    json.dump(final_data, f, indent=2)


for link in final_data:
    print(link)
