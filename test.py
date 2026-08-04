from services.supabase_client import supabase

print(supabase.storage.list_buckets())