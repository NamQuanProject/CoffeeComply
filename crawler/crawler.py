import requests
from bs4 import BeautifulSoup

def fetch_regulations(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.find_all('article')  # Customize tag according to website structure
    contents = []
    for a in articles:
        title = a.find('h2').text
        text = a.get_text()
        contents.append({"title": title, "text": text})
    return contents


def classify_text(text, role="exporter"):
    prompt = f"""
    You are an AI filter. Given the text below, answer "Yes" if it is about coffee import/export regulations, otherwise "No".

    Text:
    {text[:1000]}
    """
    response = call_llm(prompt)  # Function to use OpenAI/Mistral etc.
    return "yes" in response.lower()



def summarize(text):
    prompt = f"""
    Summarize the following regulation. Include:
    - Affected countries
    - Impact on exporters vs. farmers
    - Required actions or documents
    - Key dates or changes

    Text:
    {text[:2000]}
    """
    return call_llm(prompt)



def match_to_user(summary, user_type):
    prompt = f"""
    The user is a {user_type}. Determine if this regulation affects them and how.

    Regulation Summary:
    {summary}
    """
    return call_llm(prompt)



from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_regulation(reg):
    supabase.table("regulations").insert({
        "title": reg['title'],
        "full_text": reg['text'],
        "summary": reg['summary'],
        "country": reg['country'],
    }).execute()
