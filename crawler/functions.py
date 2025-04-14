from crawler.google_questioning import get_google_answer
from crawler.utils import read_json
from ai_service import AIAgent


def get_trade_policy_links(prompt):
    data = read_json("crawler/craw_json_data/trade_topics_links.json")  # Expecting: [(group, [list_of_links])]
    # Initial instruction to the model
    link_extraction_prompt = """Imagine you are a professional policy analyst helping to extract useful information.

    Below are grouped links about trade-related topics. Based on the user request, extract only the relevant links.

    """

    # Add grouped links
    for key, value in data.items():
        link_extraction_prompt += f"\n### Group: {key}\n"
        for link in value:
            link_extraction_prompt += f"- {link}\n"

    # Add the user query
    link_extraction_prompt += f"""\n### User Request:
{prompt}\n### Relevant Links:

    Please order the links in the order you think is the best relevant
    """

    # Run the agent
    agent = AIAgent(default_agent=True)
    response = agent.generate_response_with_structure(link_extraction_prompt, structure=list[str])
    agent.close()
    return response



def get_trade_policy_information(prompt):
    relevant_links = get_trade_policy_links(prompt)
    url_trade_policy_map = read_json("crawler/craw_json_data/url_trade_policy_map.json")
    
    information = ""
    for relevant_link in relevant_links:
        info = url_trade_policy_map.get(relevant_link)
        if info:
            information += f"{relevant_link}: {info}\n"

    final_information = f"""
    Imagine you are a specialist in analyzing trade policy. 
    Your task is to integrate the user's prompt with the most relevant policy information from official documents.

    This is the collected policy information related to the user's request:
    
    {information}

    Based on this information, what policies are directly relevant to the user's prompt: "{prompt}"?
    You can also provided link for checking up ! 
    """

    agent = AIAgent(default_agent=True)
    response = agent.generate_response(final_information)
    agent.close()
    
    return response




def get_product_information(prompt):
    agent = AIAgent(default_agent=True)
    data = read_json("crawler/craw_json_data/url_trade_policy_map.json")


    agent.close()
    pass


def get_google_additional_information(promtp):
    return get_google_answer(promtp)