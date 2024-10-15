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


def get_user_by_id(user_id):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    return response


def delete_user_from_users(name):
    response = supabase.table('users').delete().eq('name', name).execute()


def plus_one_new_follower(user_id):
    response = supabase.table('users')\
        .update({'followers': supabase.table('users').select('followers')\
                .eq('id', user_id).execute().data[0]['followers'] + 1})\
        .eq('id', user_id).execute()
