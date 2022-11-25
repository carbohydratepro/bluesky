from aozora import Db
from janome.tokenizer import Tokenizer
import collections
from tqdm import tqdm


def main():
    dbname = 'aozora_akutagawa.db'
    db = Db(dbname)
    documents = [data[3].split('。') for data in db.db_output()] #二次元配列で文章を格納
    t = Tokenizer()

    created_data = []
    for strings in (documents):
        for string in strings:
            print([token.surface for token in t.tokenize(string)])

    # for strings in tqdm(documents):
    #     for string in strings:
    #         print(sorted(collections.Counter(t.tokenize(string, wakati=True))))




if __name__ == "__main__":
    main()