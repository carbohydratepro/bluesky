import random
from aozora import Db, dataVisualization
from gensim.models.doc2vec import Doc2Vec
from janome.tokenizer import Tokenizer

def readData():
    dbname = '../bluesky_data/db/authors_famous_all.db'
    db = Db(dbname)
    data = db.db_output()
    # dataVisualization(data, ['番号', '作品名', '著者名', '本文'])
    return list(random.choice(data))

def vectorCalculate(model, text):
    t = Tokenizer()
    vector = model.infer_vector([token.surface for token in t.tokenize(text)])
    return vector

def variousDataEvaluation():
    modelname = '../bluesky_data/model/PE0201.model'

    model = Doc2Vec.load(modelname)

    data = readData()
    text = data[3]
    tag  = data[2]

    vector = vectorCalculate(model, text)

    print(data[1], data[2])
    result = model.dv.most_similar(vector)
    print(result)

def main():
    variousDataEvaluation()

if __name__ == "__main__":
    main()