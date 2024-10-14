from supabase import create_client, Client
from config import *


supabase: Client = create_client(url, key)


def add_user_to_users(name, email, password, birthday, sex):
    data = {
        'name': name,
        'email': email,
        'password': password,
        'birthday': birthday,
        'sex': sex
    }
    response = supabase.table('users').insert(data).execute()


def delete_user_from_users(name):
    response = supabase.table('users').delete().eq('name', name).execute()


