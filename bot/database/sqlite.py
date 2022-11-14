import sqlite3
import sys

from config import logger


def db_connect():
    try:
        db = sqlite3.connect('VocabularyDB.db', check_same_thread=False)
    except (sqlite3.Error, sqlite3.Warning) as err:
        logger.warning(f"He удалось подключиться к БД {err}")
        sys.exit(0)
    return db


conn = db_connect()
cursor = conn.cursor()

create_vocabulary = """
        CREATE TABLE IF NOT EXISTS `vocabulary`(
            `id` INTEGER PRIMARY KEY NOT NULL,
            `word` Varchar(50) not null,
            `translate` Varchar(50) not null
         );
        """

create_users = """
        CREATE TABLE IF NOT EXISTS `users`(
            `id` INTEGER PRIMARY KEY NOT NULL,
            `user_id` Varchar(150) not null,
            `user_name` Varchar(150) not null,
            `username` Varchar(150) not null
         );
        """

Vocabulary_table = cursor.execute(create_vocabulary)
Users_table = cursor.execute(create_users)

