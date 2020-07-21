import numpy as np
from sklearn.decomposition import PCA
import pandas as pd

# X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
# pca = PCA()
# newX = pca.fit_transform(X)
# print(X)
# print(newX)
# print(pca.components_)
# print(pca.explained_variance_ratio_)

X = pd.read_csv("E:/all.csv")
name = X['geom']
X = X.drop(columns=['geom']).to_numpy()
pca = PCA()
newX = pca.fit_transform(X)
ratio_sum = sum(pca.explained_variance_ratio_[0:19])
newX = newX[:, 0:19]
newX = pd.DataFrame(newX)
res = pd.concat([name, newX], axis=1)
res.to_csv("res.csv", header=True, index=False)
