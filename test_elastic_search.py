from serpapi import GoogleSearch
import requests



def create_question_answer(question):
    params = {
    "q": question,
    "api_key": "8fec8dd93965177b5736bd9582b7889d70d15d53e7615a6f9436c95be93715e9",
    "google_domain": "google.com",
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    for result in results['organic_results']:
        print(result['title'])
        print("Link:", result.get("link"))
        print(result['snippet'])
