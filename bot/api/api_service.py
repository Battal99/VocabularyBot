import requests


class ApiService:

    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.api_key = None

    def login(self):
        headers = {
            "Authorization": f"Basic {self.auth_token}"
        }
        url = "https://developers.lingvolive.com/api/v1/authenticate"

        get_api_key = requests.post(url=url, headers=headers)

        self.api_key = get_api_key.text.strip('"')
        return get_api_key

    def minicart_en_ru(self, word):
        url = f"https://developers.lingvolive.com/api/v1/Minicard"
        self.login()
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        params = {
            "text": word,
            "srcLang": "1033",
            "dstLang": "1049"
        }
        req = requests.get(url=url, headers=headers, params=params)
        req_json = req.json()
        if req.status_code == 200:
            result_translation = req_json["Translation"]["Translation"]
            # sounds = req_json["Translation"]["SoundName"]
        else:
            result_translation = None

        return result_translation

    def minicart_ru_en(self, word):
        url = f"https://developers.lingvolive.com/api/v1/Minicard"
        self.login()
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        params = {
            "text": word,
            "srcLang": "1049",
            "dstLang": "1033"
        }
        req = requests.get(url=url, headers=headers, params=params)
        req_json = req.json()
        if req.status_code == 200:
            result_translation = req_json["Translation"]["Translation"]
        else:
            result_translation = None

        return result_translation
