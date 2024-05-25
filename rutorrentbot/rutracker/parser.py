from bs4 import BeautifulSoup as bs
from rutracker.models import FoundFile
from typing import Optional

def search_parser(html_page: str) -> Optional[list[FoundFile]]:
    results = []
    bs_parser = bs(html_page, 'html.parser')
    # page_links = bs_parser.find_all('a', class_='med tLink tt-text ts-text hl-tags bold')
    page_links = bs_parser.find_all('tr', class_='tCenter hl-tr')
    for pl in page_links:

        object_info_tag = pl.find(class_='med tLink tt-text ts-text hl-tags bold', href=True)
        if not object_info_tag:
            print('sos')
            continue
        object_download_tag = pl.find(class_='small tr-dl dl-stub', href=True)

        data = dict()
        data['category'] = pl.find(class_='f-name').text
        data['object_name'] = object_info_tag.text
        data['object_link'] = object_info_tag.get('href')
        data['download_size'] = object_download_tag.text.replace('↓', '')
        data['download_link'] = object_download_tag.get('href')
        results.append(FoundFile(**data))

    return results

def obgject_parser(html_page: str) -> Optional[dict]:
    soup = bs(html_page, 'html.parser')
    div = soup.find_all('span', class_='post-b')
    data = {}
    magnet_link = soup.find(class_='med magnet-link', href=True)
    if magnet_link:
        magnet_link = magnet_link.get('href')
    else:
        magnet_link = None
    for br in div:
        if not isinstance(br.next_sibling, str):
            continue
        data[br.text] = br.next_sibling.replace('\n', '')
        if br.text == 'Описание':
            break
    return {'data': data, 'magnet_link': magnet_link}
    