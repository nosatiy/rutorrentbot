import asyncio
import httpx
from typing import Optional

from settings import secret
from rutracker.parser import search_parser, object_parser
from rutracker.models import FoundFile


class RTClientSession:

    def __init__(self):
        self.client_session = httpx.AsyncClient()
        self.rutracker_forum_url = 'https://rutracker.org/forum'


    async def login(self,):
        self.client_session = httpx.AsyncClient()
        body = {"login_username": secret.rutracker_login, "login_password": secret.rutracker_password, "login": "Вход"}
        method_url = self.rutracker_forum_url + '/login.php'
        response = await self.client_session.post(url=method_url, data=body)
        if response.status_code != 302:
            await self.close_session()
            # exit(1)

    async def search(self, search_string: str, light_search=True) -> Optional[list[FoundFile]]:
        method_url = self.rutracker_forum_url + f'/tracker.php?nm={search_string}'
        response = await self.client_session.get(url=method_url)
        if response.status_code != 200:
            print('bad search')
            print(response.status_code)
        search_result = search_parser(response.text)
        if not search_result:
            print('result: Could not find')
            return []
        if light_search:
            return search_result
        tasks = [self.update_search_info(page) for page in search_result]
        await asyncio.gather(*tasks)
        return search_result


    async def update_search_info(self, page: FoundFile):
        method_url = self.rutracker_forum_url + f'/{page.object_link}'
        response = await self.client_session.get(url=method_url)
        if response.status_code != 200:
            print('bad get object')
            print(response.status_code)
        object_data = object_parser(response.text)
        if not object_data:
            print('No page data')
        page.object_data = object_data['data']
        page.magnet_link = object_data['magnet_link']


    async def get_object_info(self, page_link: str, target: str = None) -> Optional[dict]:
        method_url = self.rutracker_forum_url + f'/{page_link}'
        response = await self.client_session.get(url=method_url)
        if response.status_code != 200:
            print('bad get object')
            print(response.status_code)
        object_data = object_parser(response.text)
        if not object_data:
            return
        if target == 'data':
            return object_data['data']
        if target == 'magnet':
            return object_data['magnet_link']
        return object_data

    async def close_session(self,):
        await self.client_session.aclose()
        del self.client_session

    async def reconnect(self,):
        await self.close_session()
        await self.login()

ru_session = RTClientSession()