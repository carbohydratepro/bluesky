import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.font_manager
from sklearn.manifold import TSNE
from create_model import Model
from aozora import Db
from model_evaluation import vectorCalculate

def font():
    print([f.name for f in matplotlib.font_manager.fontManager.ttflist])

def plot(model):
    pass

def main():
    dbname = '../bluesky_data/db/PE01.db'

    db = Db(dbname)
    data = db.db_output()
    modelname = '../bluesky_data/model/PE0102.model'
    m = Model(modelname).read()

    df = pd.DataFrame(data)
    weights = []
    for i in range(0, len(m.dv)):
      weights.append(m.dv[i].tolist())
    weights_tuple = tuple(weights)
    X = np.vstack(weights_tuple)

    tsne = TSNE(n_components=2, random_state = 0, perplexity = 5, n_iter = 1000)

    X_embedded = tsne.fit_transform(X)


    ddf = pd.concat([df, pd.DataFrame(X_embedded, columns = ['col1', 'col2'])], axis = 1)

    article_list = ddf[1].unique()

    colors =  ["r", "g", "b", "c", "m", "y", "k", "orange"]
    plt.figure(figsize = (16, 8))
    for i , v in enumerate(article_list):
        tmp_df = ddf[ddf[1] == v]
        plt.scatter(tmp_df['col1'],
                    tmp_df['col2'],
                    label = v,
                    color = colors[int(i/5)+1])

    plt.legend(fontsize = 5, prop={"family":"MS Gothic"})
    plt.show()

    #大量のデータを表示
    #都度学習して表示するような関数を定義


def test():
    dbname = '../bluesky_data/db/PE01.db'

    db = Db(dbname)
    data = db.db_output()
    modelname = '../bluesky_data/model/PE0102.model'
    m = Model(modelname).read()

    df = pd.DataFrame(data)
    weights = []
    for i in range(0, len(m.dv)):
      weights.append(m.dv[i].tolist())
    weights_tuple = tuple(weights)
    X = np.vstack(weights_tuple)

    tsne = TSNE(n_components=2, random_state = 0, perplexity = 5, n_iter = 1000)

    X_embedded = tsne.fit_transform(X)


    ddf = pd.concat([df, pd.DataFrame(X_embedded, columns = ['col1', 'col2'])], axis = 1)

    article_list = ddf[1].unique()

    colors =  ["r", "g", "b", "c", "m", "y", "k", "orange"]
    plt.figure(figsize = (16, 8))
    for i , v in enumerate(article_list):
        tmp_df = ddf[ddf[1] == v]
        plt.scatter(tmp_df['col1'],
                    tmp_df['col2'],
                    label = v,
                    color = colors[int(i/5)+1])

    plt.legend(fontsize = 5, prop={"family":"MS Gothic"})
    plt.show()


if __name__ == "__main__":
    test()