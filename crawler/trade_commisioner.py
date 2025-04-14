import requests
from bs4 import BeautifulSoup
from crawler.utils import get_all_links




MAIN_FARMING_LINK = "https://commission.europa.eu/food-farming-fisheries/farming_en"
all_links = get_all_links(MAIN_FARMING_LINK)
print(len(all_links))





