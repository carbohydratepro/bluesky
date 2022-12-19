# 対象の著者の作品をすべて取得する
import time
import re
import requests
import sqlite3
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from search_authors import searchAuthors
from processing_status import psm

def bookInfo(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # 情報を取得
    try:
        title = soup.find('h1', class_='title').text
        author = soup.find('h2', class_='author').text
        main_text = soup.find('div', class_='main_text').text
        # 本文から不要な記述を削除
        remove_text = ['\n', r'\u', '\r', '\u3000']
        for rt in remove_text:
            main_text = main_text.replace(rt, '')
        main_text = re.sub('\d{1,}［＃「\d{1,}」は縦中横］', '', main_text)
        return [title, author, main_text]

    except:
        pass


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
    temp = []
    url_pattern = re.compile('\.\./cards/\d{6}/card\d{1,}\.html')
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    for link in soup.find('ol').find_all('a'):
        get_url = link.get('href')
        if url_pattern.match(get_url):
            temp.append(urljoin(url, get_url))

    return temp
    # for tag in soup.find_all('ol'):
    #     for link in tag.find_all('a'):
    #         urls.append(urljoin(url, link.get("href")))

def isFile(file_name):
    return os.path.isfile(file_name)

##データベースの
class Db():
    def __init__(self,dbname):
        self.db=dbname

    def db_create(self):
        conn=sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute(
            '''CREATE TABLE books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title STRING,
            author STRING,
            body TEXT)'''
        )
        conn.commit()
        conn.close()

    def db_input(self,article):
        #値をデータベースに格納
        conn=sqlite3.connect(self.db)
        cur = conn.cursor()
        sql = 'INSERT INTO books (title, author, body) values (?,?,?)'
        cur.execute(sql, article)
        conn.commit()
        cur.close()
        conn.close()

    def db_output(self):
        #データベースから値を抽出
        conn=sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute('SELECT * from books')
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

def scraping(url, dbname):
    db=Db(dbname)
    # dbが存在しなければ作成
    if not isFile(dbname):
        db.db_create()

    urls = urlAcquisition(url)
    for url in tqdm(urls):
        article = (clickDetail(url))
        db.db_input(article)
        time.sleep(1)



def main():
    dbname = './db/authors_limit300.db'
    db=Db(dbname)
    # dbが存在しなければ作成
    if not isFile(dbname):
        db.db_create()

    author_urls = searchAuthors()
    author_count = 0
    for author_url in author_urls:
        author_count += 1
        urls = urlAcquisition(author_url[1])
        txt = str(author_url[0]) + "　取得中　" + str(author_count) + "/" + str(len(author_urls))
        psm(txt)
        for url in tqdm(urls):
            article = (clickDetail(url))
            db.db_input(article)
            time.sleep(1)


def check():
  dbname = './db/authors_limit300.db'
  db = Db(dbname)
  data = db.db_output()
  print(data)

def test():
  print(bookInfo("https://www.aozora.gr.jp/cards/000879/files/43365_26114.html"))

# soup.find('div', {'class': 'main_text'}).get_text().strip('\r''\n''\u3000').split('。')

if __name__ == "__main__":
    check()