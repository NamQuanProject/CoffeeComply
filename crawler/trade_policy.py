
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from ai_service import AIAgent
from tqdm import tqdm

MAIN_TRATE_LINK = "https://policy.trade.ec.europa.eu/trade-topics_en"
TOPIC_CATEGORY = [
    "eu-trade-relationships-country-and-region", 
    "development-and-sustainability", 
    "enforcement-and-protection", 
    "help-exporters-and-importers", 
    "analysis-and-assessment"
]


def extract_trade_policy():
    main_topics = []
    agent = AIAgent(default_agent=True)
    response = requests.get(MAIN_TRATE_LINK)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')

        # Dictionary to collect unique links by category
        category_links = {cat: set() for cat in TOPIC_CATEGORY}

        for link in links:
            href = link.get('href')
            if not href or '?' in href:
                continue

            full_url = urljoin(MAIN_TRATE_LINK, href)

            for category in TOPIC_CATEGORY:
                if category in full_url:
                    category_links[category].add(full_url)
                    break

        # Convert to desired JSON format
        for category in tqdm(TOPIC_CATEGORY):
            subtopics = []
            for url in tqdm(sorted(category_links[category])):
                # Extract the last part after '/'
                subtopic_name = url.rstrip('/').split('/')[-1]
                

                if subtopic_name.endswith("_en"):
                    subtopic_name = subtopic_name[:-3]  

                # Assign language code based on the suffix (e.g., '_en' -> 'en')
                language = "en" if subtopic_name.endswith("_en") else "unknown"
                raw_content = agent.fetch_full_text(url)
                # Append the subtopic with the desired information
                subtopics.append({
                    "name": subtopic_name,
                    "url": url,
                    "description": raw_content,
                    "summary": "",
                })

            # Add the main topic with its subtopics and language info
            main_topics.append({
                "title": category,
                "subtopics": subtopics,
                "language": language  # You can adjust this if needed, e.g., handle multiple languages
            })


        # Save to JSON file
        with open("main_and_subtopics.json", "w", encoding="utf-8") as f:
            json.dump(main_topics, f, ensure_ascii=False, indent=2)

        print("Structured JSON saved to 'main_and_subtopics.json'.")

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")




