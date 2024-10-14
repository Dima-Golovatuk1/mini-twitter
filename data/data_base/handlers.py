from supabase import create_client, Client

url = "https://igckzyzeayjxipwqpzuh.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlnY2t6eXplYXlqeGlwd3FwenVoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODc1MTY3MSwiZXhwIjoyMDQ0MzI3NjcxfQ.wmXPXkmeUUNJNhrPcFdz8qCUn1wc6bUf-LFRLrGS4HU"

supabase: Client = create_client(url, key)



# response = (
#     supabase.table("users")
#     .insert({"name": "Denmarkhf",
#              'email': 'adafhsd@gmai;.com',
#              'password': 146831,
#              'birthday': '06-12-2000',
#              'sex': 'man'})
#     .execute()
# )
response = supabase.table("users").select("*").execute()
print(response.data[0])