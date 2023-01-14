# 対象の著者の作品をすべて取得する
# コマンド処理は未実装
import time
import re
import requests
import sqlite3
import os
import random
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from search_authors import searchAuthors
from processing_status import psm
from difflib import SequenceMatcher

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

    def db_update(self, command):
        conn=sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute(command)

        conn.commit()
        cur.close()
        conn.close()

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
    dbname = '../bluesky_data/db/PE02.db'

    db=Db(dbname)
    # dbが存在しなければ作成
    if not isFile(dbname):
        db.db_create()

    errors = []

    author_urls = searchAuthors()
    author_count = 0
    for author_url in list(reversed(author_urls)):
        author_count += 1
        urls = urlAcquisition(author_url[1])
        txt = str(author_url[0]) + "　取得中　" + str(author_count) + "/" + str(len(author_urls))
        psm(txt)
        for i, url in enumerate(tqdm(urls)):
            article = (clickDetail(url))
            try:
                if (len(article) == 3 and SequenceMatcher(None, article[1], author_url[0]).ratio() >= 0.5): #正しいデータのみをDBに格納（作者が正しいかどうかを検証）
                    db.db_input(article)
            except TypeError as e:
                errors.append([author_url[0], i, e])
            time.sleep(1)

    for error in errors:
        print("著者名：", error[0], "\n作品番号：", error[1], "\nエラー内容：", error[2])


def check():
    dbname = '../bluesky_data/db/PE02.db'

    db = Db(dbname)
    data = db.db_output()
    authors = [[], []]
    book_num = 0
    for d in data:
        d = list(d)
        book_num += 1
        if d[2] not in authors[0]:
            authors[0].append(d[2])
            authors[1].append(1)
        else:
            authors[1][authors[0].index(d[2])] += 1

    for a, n in zip(authors[0], authors[1]):
        print(a, "：", n)

    #データベースに検索をかける
    # search_words = ["銀河鉄道の夜", "注文の多い料理店", "セロ弾きのゴーシュ", "やまなし", "どんぐりと山猫",
    #             "羅生門", "鼻", "河童", "歯車", "老年",
    #             "斜陽", "走れメロス", "津軽", "お伽草紙", "人間失格",
    #             "吾輩は猫である", "坊ちゃん", "草枕", "虜美人草", "三四郎"]

    new_data = []

    # for  sw in search_words:
    #     for d in data:
    #         d = list(d)
    #         if (SequenceMatcher(None, d[1], sw).ratio() >= 0.95):
    #             new_data.append(d[1:4])
    #             print(d[1])
    #             break

    #過去のデータを用いて新たなデータベースを生成する場合はコメントアウトを外す
    # 新しく生成したデータを削る

    data_num = 80

    f_idx = 0
    l_idx = 0

    for author_num in authors[1]:
        l_idx += author_num
        for _ in range(data_num):
            c_idx = random.randint(f_idx, l_idx-1)
            new_data.append(data[c_idx][1:4])
            data.pop(c_idx)
            l_idx -= 1
        f_idx = l_idx


    new_dbname = '../bluesky_data/db/PE07.db'
    reuse(new_dbname, new_data)

    new_dbname = '../bluesky_data/db/PE07-test.db'
    data = [d[1:4] for d in data]
    reuse(new_dbname, data)

def reuse(dbname, data):
    db = Db(dbname)
    # dbが存在しなければ作成
    if not isFile(dbname):
        db.db_create()

    for d in data:
        db.db_input(d)

def test():
  print(bookInfo("https://www.aozora.gr.jp/cards/000879/files/43365_26114.html"))

def shapeUp(text, pattern):
    text = re.sub(pattern, '', text)
    return text

def update(command=None):
    dbname = '../bluesky_data/db/PE02.db'

    db=Db(dbname)
    if command == None:
        command = 'SELECT * FROM books LIMIT 1'
    db.db_update(command)
    data = db.db_output()
    dataVisualization(data, ['番号', '作品名', '著者名', '本文'])
    # データ更新
    #cur.execute('UPDATE db名 SET カラム名 = "変更後" WHERE カラム名 = "変更前"')

    # データ削除
    #cur.execute('DELETE FROM persons WHERE name = "Suzuki"')

    #'UPDATE books SET author = "芥川龍之介" WHERE author = "芥川竜之介"'
    check()

# soup.find('div', {'class': 'main_text'}).get_text().strip('\r''\n''\u3000').split('。')

def dataVisualization(data, columns):
    df = pd.DataFrame(data, columns=columns)
    print(df)


if __name__ == "__main__":
    check()