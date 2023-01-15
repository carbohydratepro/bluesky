import random
from aozora import Db, dataVisualization
from gensim.models.doc2vec import Doc2Vec
from janome.tokenizer import Tokenizer
from tqdm import tqdm

def readData(dbname=None): #任意のデータベースを読み込む関数
    if dbname == None:
        dbname = '../bluesky_data/db/authors_famous_all.db'
    db = Db(dbname)
    data = db.db_output()
    # dataVisualization(data, ['番号', '作品名', '著者名', '本文'])
    return data

def randomChoice(data):#配列の中からランダムなひとつのデータを返す関数
    return list(random.choice(data))

def vectorCalculate(model, text): #引数からベクトルを求める関数
    t = Tokenizer()
    vector = model.infer_vector([token.surface for token in t.tokenize(text)])
    return vector

def variousDataEvaluation(): #でっかいデータから著者推定を行う関数
    modelname = '../bluesky_data/model/PE0201.model'

    model = Doc2Vec.load(modelname)

    data = readData()
    data = randomChoice(data)
    text = data[3]
    tag  = data[2]

    vector = vectorCalculate(model, text)

    print(data[1], data[2])
    result = model.dv.most_similar(vector)
    print(result)

def testDataEvaluation(modelname, dbname): #教師用データで学習したモデルをテストデータで解析する関数
    model = Doc2Vec.load(modelname)
    data = readData(dbname)

    evaluation_value = {'correct':0, 'incorrect':0}
    for d in tqdm(data):
        vector = vectorCalculate(model, d[2])
        result = model.dv.most_similar(vector)
        if d[2] == result[0][0]:
            evaluation_value['correct'] += 1
        else:
            evaluation_value['incorrect'] += 1

    print(evaluation_value)
    return evaluation_value['correct'] / (evaluation_value['correct']+evaluation_value['incorrect']) * 100


def main():
    rate = testDataEvaluation('../bluesky_data/model/PE0701.model', '../bluesky_data/db/PE07-test.db')
    print("正解率：", rate, "%")

if __name__ == "__main__":
    main()