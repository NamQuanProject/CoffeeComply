import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json

def get_all_links(url):
    """Fetch all hyperlinks from a given URL, returning absolute URLs."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        links = set()
        for a_tag in soup.find_all("a", href=True):
            full_url = urljoin(url, a_tag["href"])
            links.add(full_url)

        return list(links)
    except requests.RequestException as e:
        print(f"[Error] {url} -> {e}")
        return []




def read_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp '{file_path}'")
    except json.JSONDecodeError:
        print(f"Lỗi: Không thể phân tích cú pháp JSON trong tệp '{file_path}'")
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
    return None

def get_links_recursively(start_url, visited_urls=None, depth=0, max_depth=5):
    """Get links from the start URL and then get links from each of those links recursively."""
    if visited_urls is None:
        visited_urls = set()
    
    all_collected_links = set()

    if depth > max_depth:
        return all_collected_links

    if start_url not in visited_urls:
        visited_urls.add(start_url)
        first_level_links = get_all_links(start_url)
        print(f"Found {len(first_level_links)} links on level {depth} page: {start_url}")

        all_collected_links.update(first_level_links)

    
        for link in first_level_links:
            print(f"Fetching links from level {depth + 1} page: {link}")
            second_level_links = get_links_recursively(link, visited_urls, depth + 1, max_depth)
            all_collected_links.update(second_level_links)

            time.sleep(0.5)

    return all_collected_links




def safe_request(url, headers=None, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 429:
                print(f"429 Too Many Requests for {url}, waiting...")
                time.sleep(5 * (attempt + 1))
                continue
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Request error: {e}")
            time.sleep(2)
    return None



