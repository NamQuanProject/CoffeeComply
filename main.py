from ai_service import AIAgent
from crawler.trade_policy import extract_trade_policy
from crawler.utils import get_all_links, get_links_recursively





MAIN_FARMING_LINK = "https://policy.trade.ec.europa.eu/help-exporters-and-importers/import-and-export-rules_en"
all_links = get_links_recursively(MAIN_FARMING_LINK)
print(all_links)
print(len(all_links))
