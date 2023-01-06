import pickle
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from create_model import Model
from sklearn.manifold import TSNE

#形態素分解した後のデータフレームはすでにpickle化して持っている状態を想定
# with open('df_wakati.pickle', 'rb') as f:
#     df = pickle.load(f)

# #tf-idfを用いてベクトル化
# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(df[3])

#t-SNEで次元削減
def plot(df, X):
    tsne = TSNE(n_components=2, random_state = 0, perplexity = 30, n_iter = 1000)
    X_embedded = tsne.fit_transform(X)

    ddf = pd.concat([df, pd.DataFrame(X_embedded, columns = ['col1', 'col2'])], axis = 1)

    article_list = ddf[1].unique()

    colors =  ["r", "g", "b", "c", "m", "y", "k", "orange","pink"]
    plt.figure(figsize = (30, 30))
    for i , v in enumerate(article_list):
        tmp_df = ddf[ddf[1] == v]
        plt.scatter(tmp_df['col1'],
                    tmp_df['col2'],
                    label = v,
                    color = colors[i])

    plt.legend(fontsize = 30)

def main():
    modelname = '../bluesky_data/model/akuta_dazai_limit20.model'
    model = Model(modelname).read()

    plot(a, model) #タグ付け（芥川とか）、芥川と太宰の文書20ずつのモデルを作成してデータプロットできるか検証


if __name__ == "__main__":
    main()