from sqlite3 import OperationalError

from config import logger
from database.sqlite import cursor, conn


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

# for i in range(7):
#     await asyncio.sleep(60*60*24)
#     await bot.send_message(user_id, MSG.format(user_name))