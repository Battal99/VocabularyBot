import os
import logging
import sys
import dotenv

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

dotenv.load_dotenv(".env")


BOT_API_KEY = os.environ['BOT_API_KEY']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
