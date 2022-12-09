import re
import requests
import aozora
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from processing_status import psm

def search_urls(url, pattern, text_search=False, lower=20): # pattern：正規表現
    urls = []
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # patternに一致するURLを取得
    url_pattern = re.compile(pattern)
    for link in soup.find_all('a'):
        get_url = link.get('href')
        if type(get_url) is str and url_pattern.match(get_url):
            temp_url = urljoin(url, get_url)
            if text_search:
                book_num = re.sub(r"\D", "", link.parent.text)
                if int(book_num) > lower:
                    text = link.text
                    urls.append([text, temp_url])
            else:
                urls.append(temp_url)


    return urls


def search_authors():
    a_rows = search_urls('https://www.aozora.gr.jp/', 'index_pages/person_.+\.html') #url, 著者名

    author_urls = []
    psm("対象の著者URL取得完了")
    for a_row in tqdm(a_rows):
        author_urls += search_urls(a_row, 'person\d{1,}\.html#sakuhin_list_1', True, lower=100)
        time.sleep(1)

    # for author in authors():
    #     aozora.scraping(author[0], author[1])


def main():
    search_authors()


if __name__ == "__main__":
    main()