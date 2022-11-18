import time
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def bookInfo(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # 情報を取得
    title = soup.find('h1').text
    author = soup.find('h2').text
    main_text = soup.find('div').text

    # 本文から不要な記述を削除
    remove_text = ['\n', r'\u', '\r', '\u3000']
    for rt in remove_text:
        main_text = main_text.replace(rt, '')
    main_text = re.sub('\d{1,}［＃「\d{1,}」は縦中横］', '', main_text)

    return [title, author, main_text]


def clickDetail(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    url_pattern = re.compile('\./files/\d{1,}_\d{1,}.html')
    for tag in soup.find('body').find_all('div'):
        for link in tag.find_all('a'):
            get_url = link.get('href')
            if url_pattern.match(get_url):
                url = urljoin(url, get_url)
                break

    return bookInfo(url)


def urlAcquisition(url):
    url_pattern = re.compile('\.\./cards/\d{6}/card\d{1,}\.html')
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    for link in soup.find('ol').find_all('a'):
        get_url = link.get('href')
        if url_pattern.match(get_url):
            urls.append(urljoin(url, get_url))
    # for tag in soup.find_all('ol'):
    #     for link in tag.find_all('a'):
    #         urls.append(urljoin(url, link.get("href")))




urls = []
book_info = []
urlAcquisition('https://www.aozora.gr.jp/index_pages/person879.html#sakuhin_list_1')
for url in urls:
    print(clickDetail(url))
    time.sleep(1)

# soup.find('div', {'class': 'main_text'}).get_text().strip('\r''\n''\u3000').split('。')

