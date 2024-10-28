from supabase import create_client, Client
from data.data_base.config import key, url

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


def get_users():
    response = supabase.table('users').select('*').execute()
    return response.data


def get_user_by_id(user_id):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    if response.data:
        return response.data[0]
    else:
        return None


def get_users_by_email(email):
    response = supabase.table("users").select("*").eq("email", email).execute()
    return response.data


def delete_user_from_users(name):
    response = supabase.table('users').delete().eq('name', name).execute()


def create_new_post(user_id, title, content, image_url, video_url):
    data = {
        'user_id': user_id,
        'title': title,
        'content': content,
        'image_url': image_url,
        'video_url': video_url
    }
    response = supabase.table('posts').insert(data).execute()


def delete_post_by_id(id):
    response = supabase.table('posts').delete().eq('id', id).execute()


def get_all_posts():
    response = supabase.table('posts').select('*').execute()
    return response.data


def get_all_posts_by_user_id(user_id):
    response = supabase.table('posts').select('*').eq('user_id', user_id).execute()
    return response.data


def get_post_by_id(id):
    response = supabase.table('posts').select('*').eq('id', id).execute()
    return response.data


def add_comment(user_id, post_id, comment):
    data = {
        'user_id': user_id,
        'post_id': post_id,
        'comment': comment
    }
    response = supabase.table('comments').insert(data).execute()


def get_all_comments_by_post_id(id):
    response = supabase.table('comments').select('*').eq('post_id', id).execute()
    return response.data


def delete_comment_by_id(comment_id):
    response = supabase.table('comments').delete().eq('id', comment_id).execute()


def delete_post_by_title_and_user_id(title, user_id):
    response = supabase.table('posts').delete().eq('title', title).eq('user_id', user_id).execute()
    return response


def get_post_by_title_and_user_id(title, user_id):
    response = supabase.table('posts').select('*').eq('title', title).eq('user_id', user_id).execute()

    if response.data:
        return response.data[0]
    return None


def get_post_by_title(title):
    response = supabase.table('posts').select('*').eq('title', title).execute()
    return response.data


def get_post_by_title_partial(title):
    response = supabase.table('posts').select('*').ilike('title', f'%{title}%').execute()
    return response.data


def add_new_follower(user_id: int, follower_id: int):
    data = {
        'user_id': follower_id,
        'follower_id': user_id
    }
    response = supabase.table('followers').insert(data).execute()


def remove_follower(user_id: int, follower_id: int):
    response = supabase.table('followers').delete().eq('user_id', user_id).eq('follower_id', follower_id).execute()


def get_followers_by_user_id(user_id: int):
    if response.data:
        return [item['follower_id'] for item in response.data[::]]
    else:
        return []


def get_comments_by_user_id_and_post_id(user_id, post_id):
    response = supabase.table('comments').select('*').eq('user_id', user_id).eq('post_id', post_id).execute()
    return response.data


def get_comment_by_id(id):
    response = supabase.table('comments').select('*').eq('id', id).execute()
    return response.data


def get_user_id_by_post_id(post_id):
    response = supabase.table('posts').select('*').eq('id', post_id).execute()
    if response.data:
        return response.data[0]['user_id']
    return []


def is_following(user_id: int, follower_id: int) -> bool:
    response = supabase.table('followers').select('*').eq('user_id', user_id).eq('follower_id', follower_id).execute()
    return len(response.data) > 0 if response.data else False