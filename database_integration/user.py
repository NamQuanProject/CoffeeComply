from supabase import create_client, Client

from dotenv import load_dotenv
import os
load_dotenv()






class DatabaseIntergration():
    def __init__(self, url, key, default_settings):
        if (default_settings):
            url = os.environ["SUPABASE_URL"]
            key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
        self.supabase_url = url
        self.supabase_key = key
        self.supabase_client: Client = create_client(self.supabase_url,self.supabase_key)






        
        