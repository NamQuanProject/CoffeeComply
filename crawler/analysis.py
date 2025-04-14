
from dotenv import load_dotenv
from ai_service import AIAgent
from crawler import get_google_answer, get_trade_policy_information, get_product_information
import os
load_dotenv()


def handleUserPrompt(prompt, specific_user):
    agent = AIAgent(default_agent=True)
    agent.model_name = "gemini-2.0-flash"
    

    relevant_policy_info = get_trade_policy_information(prompt)
    google_search_information = get_google_answer(question=prompt)

    product_info = get_product_information(prompt)


    final_prompt = f"""
    You are a professional trade and market advisor specializing in international commerce, investment frameworks, and product-specific export strategies.

    A user who is {specific_user} is seeking guidance on the following topic:
    → "{prompt}"

    To assist them, use the following curated data:

    📘 **Relevant Trade Policy Information**:
    {relevant_policy_info}

    🌐 **Insights from Google/Web Search**:
    {google_search_information}

    📦 **Product & Market-Specific Information**:
    {product_info}

    🎯 **Your task**:
    - Provide a clear, well-structured, and actionable response.
    - Use policy terms and market terminology appropriately.
    - Highlight trade opportunities, regulatory constraints, export incentives, and market access rules.
    - If applicable, suggest next steps or useful contacts (like government agencies or agreements to explore).

    Make sure your tone is professional, informative, and supportive—similar to a consulting report given to an investor or business operator.
    """

    response = agent.generate_response(final_prompt)
    agent.close()
    return response
    