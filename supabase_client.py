from supabase import create_client, Client
from dotenv import load_dotenv
import os
SUPABASE_URL = "https://byymlfhjzyieeepkedap.supabase.co"

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ5eW1sZmhqenlpZWVlcGtlZGFwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ2MDQxMDYsImV4cCI6MjA2MDE4MDEwNn0.ZzGYEdZE0LG8alQ9_1Hz7sB4oMtfcohjYQyARHfTFec"

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)
