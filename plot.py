import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from create_model import Model
from aozora import Db
from gensim.models.doc2vec import Doc2Vec
from sklearn.feature_extraction.text import TfidfVectorizer

def plot(model):
    pass

def main():
    dbname = '../bluesky_data/db/PE01.db'

    db = Db(dbname)
    data = db.db_output()
    modelname = '../bluesky_data/model/PE0101.model'
    m = Model(modelname).read()

    df = pd.DataFrame(data)
    weights = []
    for i in range(0, len(m.dv)):
      weights.append(m.dv[i].tolist())
    weights_tuple = tuple(weights)
    X = np.vstack(weights_tuple)

    tsne = TSNE(n_components=2, random_state = 0, perplexity = 3, n_iter = 1000)

    X_embedded = tsne.fit_transform(X)


    ddf = pd.concat([df, pd.DataFrame(X_embedded, columns = ['col1', 'col2'])], axis = 1)

    article_list = ddf[1].unique()

    colors =  ["r", "g", "b", "c", "m", "y", "k", "orange","pink","r", "g", "b", "c", "m", "y", "k", "orange","pink"]
    plt.figure(figsize = (30, 30))
    for i , v in enumerate(article_list):
        tmp_df = ddf[ddf[1] == v]
        plt.scatter(tmp_df['col1'],
                    tmp_df['col2'],
                    label = v,
                    color = colors[i])

    plt.legend(fontsize = 30)
    plt.show()



if __name__ == "__main__":
    main()