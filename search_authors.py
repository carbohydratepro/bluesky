import re
import requests
import time
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from processing_status import psm

def searchUrls(url, pattern, text_search=False, lower=20, authors=None): # pattern：正規表現
    urls = []
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    time = 0
    # patternに一致するURLを取得
    url_pattern = re.compile(pattern)
    for link in soup.find_all('a'):
        get_url = link.get('href')
        if type(get_url) is str and url_pattern.match(get_url):
            temp_url = urljoin(url, get_url)
            if text_search:
                book_num = re.sub(r"\D", "", link.parent.text)
                if int(book_num) > lower:
                    if authors is None or link.text in authors:
                        time += int(book_num)
                        text = link.text
                        urls.append([text, temp_url])
            else:
                urls.append(temp_url)

    return urls, time


def searchAuthors():
    a_rows, temp = searchUrls('https://www.aozora.gr.jp/', 'index_pages/person_.+\.html') #url, 著者名

    author_urls = []
    a_time = 0
    lower_limit = 1
    target_authors = ["宮沢 賢治", "芥川 竜之介", "太宰 治", "夏目 漱石"]
    psm("対象の著者URL取得中")
    for a_row in tqdm(a_rows):
        url, ts = searchUrls(a_row, 'person\d{1,}\.html#sakuhin_list_1', True, lower=lower_limit, authors=target_authors)
        author_urls += url
        a_time += ts
        time.sleep(1)

    print("予想取得完了時間は：", datetime.timedelta(seconds=(a_time*1.5)))
    # for author in authors():
    #     aozora.scraping(author[0], author[1])

    return author_urls


def main():
    urls = searchAuthors()
    print(urls)


if __name__ == "__main__":
    main()