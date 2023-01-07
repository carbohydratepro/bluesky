import matplotlib.pyplot as plt
import pandas as pd
from sklearn.manifold import TSNE
from create_model import Model
import numpy as np

def plot(model):
  sentence_vectors = np.vstack(model.docvecs.vectors_docs)
  vectors_tsne = TSNE(n_components=2).fit_transform(sentence_vectors)
  print(vectors_tsne)

def main():
    modelname = '../bluesky_data/model/akuta_dazai_limit20.model'
    model = Model(modelname).read()

    plot(model) #タグ付け（芥川とか）、芥川と太宰の文書20ずつのモデルを作成してデータプロットできるか検証


if __name__ == "__main__":
    main()