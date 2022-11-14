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
)

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
                        "чтобы посмотреть словарь /show_words", parse_mode='html')


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
                                      " чтобы посмотреть словарь /show_words")
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


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
