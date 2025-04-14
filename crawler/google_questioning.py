from serpapi import GoogleSearch


def get_google_answer(question):
    question = f"Can you give me a latest news related to this {question}"
    params = {
        "q": question,
        "api_key": "8fec8dd93965177b5736bd9582b7889d70d15d53e7615a6f9436c95be93715e9",
        "google_domain": "google.com",
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])

        final_info = []
        for result in organic_results:
            title = result.get("title")
            link = result.get("link")
            snippet = result.get("snippet")

            if title and snippet:
                final_info.append({
                    "Title": title,
                    "Link": link,
                    "Snippet": snippet,
                })

        return final_info

    except Exception as e:
        print(f"Error during search: {e}")
        return []
