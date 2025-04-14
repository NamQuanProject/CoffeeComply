from supabase_client import get_supabase


def save_final_output(question: str, response: str):
    supabase = get_supabase()
    data = {"question": question, "response": response}
    supabase.table("final_output").insert(data).execute()


def save_relevant_product(question: str, response: str):
    supabase = get_supabase()
    data = {"query": question, "info": response}
    supabase.table("relevant_product_info").insert(data).execute()


def save_relevant_trade(question: str, response: str):
    supabase = get_supabase()
    data = {"query": question, "info": response}
    supabase.table("relevant_trade_info").insert(data).execute()

def save_google_search(question: str, response: str):
    supabase = get_supabase()
    data = {"query": question, "info": response}
    supabase.table("google_search_relevant_info").insert(data).execute()