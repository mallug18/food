import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)

response = supabase.table('profiles').select('*').limit(1).execute()
if response.data:
    print("Profiles columns:", list(response.data[0].keys()))
else:
    print("No data in profiles table")
