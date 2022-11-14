import asyncio
import aioschedule
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

import messages
from config import BOT_API_KEY
from database.methods import (
    insert_word_in_vocabulary,
    delete_data_in_vocabulary_table,
    get_words_in_vocabulary,
    get_word_in_vocabulary,
    get_users,
)
from event import process_after_register_views

bot = Bot(token=BOT_API_KEY)

dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    en_word = State()
    ru_word = State()


@dp.message_handler(commands="start")
async def main(message: types.Message):
    await message.reply(f"Hello,<b>{message.chat.username}</b> это англо-русский словарь. "
                        "Чтобы перевести англ слово /tr_en_ru, "
                        "чтобы перевести русское слово /tr_ru_en, "
                        "чтобы удалить все из словаря /clear_dict, "
                        "чтобы посмотреть словарь /show_words, "
                        "получить любое слово /get_word", parse_mode='html')
    process_after_register_views(message.chat.id, message.chat.username, message.chat.first_name)


@dp.message_handler(commands="tr_en_ru")
async def tr_en_ru(message: types.Message):
    await message.reply("Введите английское слово")
    await Form.en_word.set()


@dp.message_handler(commands="tr_ru_en")
async def tr_ru_en(message: types.Message):
    await message.reply("Введите русское слово")
    await Form.ru_word.set()


@dp.message_handler(state=Form.en_word)
async def translate_en_ru(message: types.Message, state: FSMContext):
    result = messages.translate_eng_word(message.text)
    if result is not None:
        await message.answer(text=result)
        insert = insert_word_in_vocabulary(message.text, result)
        if insert:
            await message.answer(text="Чтобы перевести еще раз нажмите /tr_en_ru,"
                                      " чтобы перевести русское слово /tr_ru_en,"
                                      " чтобы удалить все из словаря /clear_dict,"
                                      " чтобы посмотреть словарь /show_words,"
                                      " получить любое слово /get_word")
            await state.finish()
        else:
            await message.answer(text="Cлово не добавлено в БД")
    else:
        await message.answer(text="Введите английское слово,"
                                  " такого слова не найдено")


@dp.message_handler(state=Form.ru_word)
async def translate_ru_en(message: types.Message, state: FSMContext):
    result = messages.translate_rus_word(message.text)
    if result is not None:
        await message.answer(text=result)
        await message.answer(text="Чтобы перевести еще раз нажмите /tr_ru_en,"
                                  " чтобы перевести английское слово /tr_en_ru,"
                                  " чтобы посмотреть словарь /show_words")
        await state.finish()
    else:
        await message.answer(text="Введите русское слово,"
                                  " такого слова не найдено")


@dp.message_handler(commands="clear_dict")
async def drop_vocabulary(message: types.Message):
    delete_data_in_vocabulary_table()
    await message.reply("Словарь очищен")


@dp.message_handler(commands="show_words")
async def show_vocabulary(message: types.Message):
    words = get_words_in_vocabulary()
    await message.reply(f"Словарь: \n{words}")


@dp.message_handler(commands="get_word")
async def get_word(message: types.Message):
    word, translate = get_word_in_vocabulary()
    await message.reply(f"{word}-{translate}")


@dp.message_handler(commands="get_word")
async def get_word():
    word, translate = get_word_in_vocabulary()
    for user in get_users():
        await bot.send_message(chat_id=user, text=f"{word} - {translate}")


async def scheduler():
    aioschedule.every().day.at("10:00").do(get_word)
    aioschedule.every().day.at("12:00").do(get_word)
    aioschedule.every().day.at("14:00").do(get_word)
    aioschedule.every().day.at("16:00").do(get_word)
    aioschedule.every().day.at("17:00").do(get_word)
    aioschedule.every().day.at("18:00").do(get_word)
    aioschedule.every().day.at("19:00").do(get_word)
    aioschedule.every().day.at("20:00").do(get_word)
    aioschedule.every().day.at("22:00").do(get_word)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(scheduler())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
