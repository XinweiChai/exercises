import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

import pandas as pd
from pyproj import Proj, transform
from pyproj import Transformer
from pyspark.sql.functions import udf
from transCoordinateSystem import wgs84_to_gcj02


def transform_series(lon, lat):
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    x, y = transformer.transform(lat, lon)
    return pd.Series((x, y))


def lon_to_web_mercator(lon):
    k = 6378137
    return lon * (k * np.pi / 180.0)


def lat_to_web_mercator(lat):
    k = 6378137
    return np.log(np.tan((90 + lat) * np.pi / 360.0)) * k


def wgs84_to_web_mercator(df, lon="lon", lat="lat"):
    """Converts decimal longitude/latitude to Web Mercator format"""
    k = 6378137
    df["x"] = df[lon] * (k * np.pi / 180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * np.pi / 360.0)) * k
    return df


def precondition(df, lon='lng', lat='lat'):
    df[[lon, lat]] = df.apply(
        lambda row: wgs84_to_gcj02(row[lon], row[lat]), axis=1)
    # df[['x', 'y']] = df.apply(
    #     lambda row: transform_series(row[lon], row[lat]), axis=1)
    df = wgs84_to_web_mercator(df, lon=lon, lat=lat)
    return df


if __name__ == '__main__':
    # fn = "E:/20个城市的POI数据/POI数据整理城市/北京/CSV版本/餐饮2.csv"
    # fn = "restaurant_trans.csv"
    # fn = "resto.csv"
    # fn = "餐饮after.csv"
    name = ['ordinary_company', 'IT_company', 'mall', 'supermarket']
    for i in name:
        fn = f"C:/Users/zby11/Downloads/poi/{i}_trans.csv"
        # fn = "bike_after.csv"
        x = pd.read_csv(fn)
        coord = x[['x', 'y']]
        X = np.array(coord.values)
        # #############################################################################
        # Generate sample data
        # centers = [[1, 1], [-1, -1], [1, -1]]
        # X, labels_true = make_blobs(n_samples=30, centers=centers, cluster_std=0.4,
        #                             random_state=0)

        # X = StandardScaler().fit_transform(X)

        # #############################################################################
        # Compute DBSCAN
        db = DBSCAN(eps=1000, min_samples=10).fit(X)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        x['label'] = labels
        x = x.drop(columns=['OBJECTID'])
        # x.to_csv('resto_labeled.csv', index=False)
        x.to_csv(f'{i}_labeled.csv', index=False)

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)
        #
        print('Estimated number of clusters: %d' % n_clusters_)
        print('Estimated number of noise points: %d' % n_noise_)
    # print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    # print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    # print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    # print("Adjusted Rand Index: %0.3f"
    #       % metrics.adjusted_rand_score(labels_true, labels))
    # print("Adjusted Mutual Information: %0.3f"
    #       % metrics.adjusted_mutual_info_score(labels_true, labels))
    # print("Silhouette Coefficient: %0.3f"
    #       % metrics.silhouette_score(X, labels))

    # #############################################################################
    # Plot result
    import matplotlib.pyplot as plt

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=15)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=2)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    # plt.show()
    plt.savefig("res.png",bbox_inches='tight')
