from supabase import create_client, Client
url = "https://igckzyzeayjxipwqpzuh.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlnY2t6eXplYXlqeGlwd3FwenVoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODc1MTY3MSwiZXhwIjoyMDQ0MzI3NjcxfQ.wmXPXkmeUUNJNhrPcFdz8qCUn1wc6bUf-LFRLrGS4HU"


supabase: Client = create_client(url, key)


def add_user_to_users(name, email, password, birthday, sex):
    data = {
        'name': name,
        'email': email,
        'password': password,
        'birthday': birthday,
        'sex': sex
    }
    print(123)
    response = supabase.table('users').insert(data).execute()


def get_users():
    response = supabase.table('users').select('*').execute()
    return response.data


def get_users_by_id(user_id):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    return response.data


def get_users_by_email(email):
    response = supabase.table("users").select("*").eq("email", email).execute()
    return response.data


def delete_user_from_users(name):
    response = supabase.table('users').delete().eq('name', name).execute()


