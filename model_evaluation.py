from aozora import Db, isFile, dataVisualization
from create_model import Model
from gensim.models.doc2vec import TaggedDocument
from gensim.models.doc2vec import Doc2Vec
from gensim.utils import simple_preprocess
from janome.tokenizer import Tokenizer




def main():
    modelname = '../bluesky_data/model/PE0101.model'

    model = Doc2Vec.load(modelname)

    t = Tokenizer()
    text = """
    雨にも負けず、風にも負けず、雪にも夏の暑さにも負けぬ、丈夫な体を持ち、欲はなく、決して瞋からず、何時も静かに笑っている。
    """
    vector = model.infer_vector([token.surface for token in t.tokenize(text)])

    result = model.dv.most_similar(vector)
    print(result)

if __name__ == "__main__":
    main()