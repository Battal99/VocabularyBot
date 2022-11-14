import random
from sqlite3 import OperationalError

from config import logger
from database.sqlite import cursor, conn

from event import after_start_views


def insert_word_in_vocabulary(word, translate) -> bool:
    try:
        cursor.execute(f'insert into `vocabulary` (`word`, `translate`) values ("{word}", "{translate}");')
        conn.commit()
        return True
    except OperationalError as err:
        logger.warning(f"Ошибка занесения в БД {err}")
        return False


def delete_data_in_vocabulary_table():
    cursor.execute("DELETE FROM `vocabulary`;")
    conn.commit()


def get_words_in_vocabulary():
    word_dict = {}
    words = cursor.execute("select * from `vocabulary`;").fetchall()
    for word in words:
        word_dict[word[1]] = word[2]
    return word_dict


def get_word_in_vocabulary():
    word_dict = {}
    words = cursor.execute("select * from `vocabulary`;").fetchall()
    for word in words:
        word_dict[word[1]] = word[2]
    word, translate = random.choice(list(word_dict.items()))

    return word, translate


@after_start_views
def insert_users(user_id, user_name, username):
    info = cursor.execute('SELECT * FROM `users` WHERE user_id=?', (user_id,))
    if info.fetchone() is None:
        try:
            cursor.execute('Insert into `users` (user_id,'
                           f'user_name, username) values ("{user_id}","{user_name}","{username}");')
            conn.commit()
            return True
        except OperationalError as err:
            logger.warning(f"Ошибка занесения в БД {err}")
    else:
        logger.info(f"Пользователь есть в БД")
    return False


def get_users():
    users_list = []
    users = cursor.execute('SELECT * FROM `users`;').fetchall()
    for user in users:
        users_list.append(user[1])
    return users_list
