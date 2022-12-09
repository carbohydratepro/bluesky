from aozora import Db, isFile
from janome.tokenizer import Tokenizer
from tqdm import tqdm
from gensim.models.doc2vec import TaggedDocument
from gensim.models.doc2vec import Doc2Vec


##モデルの
class Model():
    def __init__(self, modelname):
        self.modelname=modelname

    # 保存
    def save(self, model):
        model.save(self.modelname)

    # 読み込み
    def read(self):
        return Doc2Vec.load(self.modelname)

    # 削除
    def delete(self):
        pass



def create(modelname):
    dbname = 'aozora_akutagawa.db'
    db = Db(dbname)
    documents = [data[3] for data in db.db_output()] #二次元配列で文章を格納
    t = Tokenizer()

    created_data = []
    count = 0

    for strings in tqdm(documents):
        created_data.append(TaggedDocument([token.surface for token in t.tokenize(strings)], [count]))
        count += 1

    model = Doc2Vec(created_data, dm=1, vector_size=200, min_count=10, epochs=20)
    Model(modelname).save(model)



def main():
    modelname = 'akutagawa_test.model'
    if not isFile(modelname):
        create(modelname)

    model = Model(modelname).read()
    print(model.docvecs.most_similar(10))

if __name__ == "__main__":
    main()