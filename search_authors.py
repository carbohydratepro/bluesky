import re
import requests
import aozora
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

def search_urls(url, pattern): # pattern：正規表現
    urls = []
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # patternに一致するURLを取得
    url_pattern = re.compile(pattern)
    for link in soup.find_all('a'):
        get_url = link.get('href')
        if type(get_url) is str and url_pattern.match(get_url):
            temp_url = urljoin(url, get_url)
            urls.append(temp_url)
    return urls


def search_authors():
    authors = search_urls('https://www.aozora.gr.jp/', 'index_pages/person_.+\.html') #url, 著者名

    print(authors)
    # for author in authors():
    #     aozora.scraping(author[0], author[1])


def main():
    search_authors()


if __name__ == "__main__":
    main()