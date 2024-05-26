import os
import logging
from dotenv import load_dotenv
from attr import dataclass
load_dotenv()


logging.basicConfig(level=logging.INFO)

@dataclass
class Secret:
    bot_token: str = os.environ.get('bot_token')
    rutracker_login: str = os.environ.get('rutracker_login')
    rutracker_password: str = os.environ.get('rutracker_password')

secret = Secret()