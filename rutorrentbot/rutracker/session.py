import asyncio
import httpx
import functools
import logging
from typing import Optional
from datetime import datetime, timedelta

from settings import secret
from rutracker.parser import search_parser, object_parser
from rutracker.models import FoundFile


class RTClientSession:

    def __init__(self):
        self.client_session = httpx.AsyncClient()
        self.last_session_update = datetime.now()
        self.rutracker_forum_url = 'https://rutracker.org/forum'

    def retry(func, retry_count: int = 2):

        @functools.wraps(func)
        async def retry_(self, *args, **kwargs):
            if datetime.now() - self.last_session_update > timedelta(hours=3):
                await self.reconnect()
            for try_ in range(retry_count): 
                try:
                    result = await func(self, *args, **kwargs)
                    return result
                except Exception as error:
                    logging.error(msg=error)
                    await self.reconnect()
            
        return retry_
    
    async def close_session(self,):
        await self.client_session.aclose()

    async def reconnect(self,):
        await self.close_session()
        self.client_session = httpx.AsyncClient()
        self.last_session_update = datetime.now()
        await self.login()

    async def login(self,):
        body = {"login_username": secret.rutracker_login, "login_password": secret.rutracker_password, "login": "Вход"}
        method_url = self.rutracker_forum_url + '/login.php'
        response = await self.client_session.post(url=method_url, data=body)
        if response.status_code != 302:
            raise 'error login'

    @retry
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

    @retry
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

    @retry
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

ru_session = RTClientSession()