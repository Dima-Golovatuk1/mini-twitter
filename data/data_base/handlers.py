import psycopg2
import logging


from config import *


def get_db_connection():
    connection = psycopg2.connect(
        host=host,
        database=db_name,
        user=user,
        password=password
    )
    return connection


def get_post_by_id(post_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT post_name, content FROM posts WHERE id = %s"
    cursor.execute(query, (post_id,))
    post = cursor.fetchone()
    cursor.close()
    connection.close()

    if post:
        post_name, content = post
        return {
            'post_name': post_name,
            'content': content
        }
    else:
        return None


def add_new_user(name: str, email: str, hash_password: str, birthday: str, sex: str):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """INSERT INTO users (id, name, email, password, birthday, sex) VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(
            query, (1, name, email, hash_password, birthday, sex)
        )
        connection.commit()
        return "success"

    except Exception as ex:
        logging.error('[INFO] Error while working with PostgreSQL', exc_info=True)

    finally:
        if connection:
            cursor.close()
            connection.close()
            logging.info('[INFO] PostgreSQL connection closed')


def look_user_by_id(_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """SELECT name, email, password, birthday, sex FROM users WHERE id = %s"""
        cursor.execute(query, (_id,))
        user = cursor.fetchone()
        if user:
            return {
                "name": user[0],
                "email": user[1],
                "password": user[2],
                "birthday": user[3],
                "sex": user[4]
            }
        else:
            return "User not found"

    except Exception as ex:
        logging.error('[INFO] Error while working with PostgreSQL', exc_info=True)

    finally:
        if connection:
            cursor.close()
            connection.close()
            logging.info('[INFO] PostgreSQL connection closed')
            