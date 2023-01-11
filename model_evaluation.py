import random
from aozora import Db, isFile, dataVisualization
from create_model import Model
from gensim.models.doc2vec import TaggedDocument
from gensim.models.doc2vec import Doc2Vec
from gensim.utils import simple_preprocess
from janome.tokenizer import Tokenizer

def readData():
    dbname = '../bluesky_data/db/authors_famous_all.db'
    db = Db(dbname)
    data = db.db_output()
    # dataVisualization(data, ['番号', '作品名', '著者名', '本文'])
    return list(random.choice(data))


def main():
    modelname = '../bluesky_data/model/PE0102.model'

    model = Doc2Vec.load(modelname)

    t = Tokenizer()
    data = readData()
    text = data[3]

    vector = model.infer_vector([token.surface for token in t.tokenize(text)])

    print(data[1], data[2])
    result = model.dv.most_similar(vector)
    print(result)

if __name__ == "__main__":
    main()