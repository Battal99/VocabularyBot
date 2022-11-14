from api.api_service import ApiService
from config import AUTH_TOKEN


api_client = ApiService(AUTH_TOKEN)


def translate_rus_word(word) -> str | None:
    result = api_client.minicart_ru_en(word)
    return result


def translate_eng_word(word) -> str | None:
    result = api_client.minicart_en_ru(word)
    return result
