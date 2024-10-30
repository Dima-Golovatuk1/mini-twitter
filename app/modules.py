from flask_login import UserMixin
from data.data_base.handlers import get_user_by_id


class User(UserMixin):
    def __init__(self, id, email, name, password, DOB, gender, rem=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.DOB = DOB
        self.gender = gender
        self.rem = rem

    def remember(self):
        return self.rem == 'on'

    def get_id(self):
        return str(self.id)


def load_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return User(id=user['id'], email=user['email'], name=user['name'], password=user['password'],
                    DOB=user['birthday'], gender=user['sex'])
    return None


def get_embed_url(video_url):
    if not video_url:
        return None

    if "tiktok.com" in video_url:
        video_id = video_url.split('/')[-1].split('?')[0]
        return f"https://www.tiktok.com/embed/{video_id}"

    if "youtube.com" in video_url:
        if "watch?v=" in video_url:
            video_url = video_url.replace("watch?v=", "embed/")
        elif "/shorts/" in video_url:
            video_id = video_url.split("/shorts/")[-1].split('?')[0]
            video_url = f"https://www.youtube.com/embed/{video_id}"
    elif "youtu.be" in video_url:
        video_id = video_url.split('/')[-1].split('?')[0]
        video_url = f"https://www.youtube.com/embed/{video_id}"

    if "&" in video_url:
        video_url = video_url.split("&")[0]

    if "vimeo.com" in video_url:
        video_id = video_url.split('/')[-1].split('?')[0]
        video_url = f"https://player.vimeo.com/video/{video_id}"

    return video_url