import requests
import json
import os

# workspace = 'aquaculture'
workspace = 'aqua_cluster'
db_ip = '172.168.2.164'
db = 'aqua'
pw = 'postgres'
username = 'postgres'
# url_base = 'http://localhost:8080/geoserver/rest/'
url_base = 'http://172.169.0.6:8080/geoserver/rest/'

for i in os.listdir('data/3-level'):
    path = 'E:/exercises/aquaculture/'
    # get data and compress to zip
    # os.system(f'pgsql2shp -f data/{i}_cluster.shp -h {ip} -P {pw} -u {username} {db} '
    #           f'\"SELECT CAST(sum_area AS Integer) AS sum_area, geom FROM {i}.{i}_cluster\"')
    # os.system(f'7z u data/{i}_clusters.zip {path}data/{i}_cluster.*')
    os.system(f'pgsql2shp -f data/{i}.shp -h {db_ip} -P {pw} -u {username} {db} '
              f'\"SELECT cat,area,geom FROM {i}.{i}\"')
    os.system(f'7z u data/{i}_data.zip {path}data/{i}.*')
    auth = ('admin', 'geoserver')
    # url_cluster_store = url_base + 'workspaces/' + workspace + '/datastores/' + i + '_clusters/'
    url_store = url_base + 'workspaces/' + workspace + '/datastores/' + i + '/'
    # upload data to store
    # x = requests.put(url_cluster_store + 'file.shp', auth=auth, headers={'content-type': 'application/zip'},
    #                  data=open(f'data/{i}_clusters.zip', 'rb').read())
    x = requests.put(url_store + 'file.shp', auth=auth, headers={'content-type': 'application/zip'},
                     data=open(f'data/{i}_data.zip', 'rb').read())
    print(x)
    # url_cluster_feature = url_cluster_store + 'featuretypes/' + i + '_cluster.json'
    # url_cluster_layer = url_base + 'layers/' + workspace + ':' + i + '_cluster.json'
    url_feature = url_store + 'featuretypes/' + i + '.json'
    url_layer = url_base + 'layers/' + workspace + ':' + i + '.json'
    headers = {'content-type': 'application/json'}

    # set projection of feature
    # x = requests.get(url_cluster_feature, auth=auth, headers=headers)
    # y = x.json()
    # y['featureType']['srs'] = 'EPSG:3857'
    # x = requests.put(url_cluster_feature, auth=auth, headers=headers, data=str(y))
    # print(x)

    x = requests.get(url_feature, auth=auth, headers=headers)
    y = x.json()
    y['featureType']['srs'] = 'EPSG:4326'
    x = requests.put(url_feature, auth=auth, headers=headers, data=str(y))
    print(x)

    # set layer style
    # x = requests.get(url_cluster_layer, auth=auth, headers=headers)
    # y = x.json()
    # y['layer']['defaultStyle']['name'] = workspace + ':static_cluster'
    # x = requests.put(url_cluster_layer, auth=('admin', 'geoserver'), headers=headers, data=str(y))
    # print(x)

    x = requests.get(url_layer, auth=auth, headers=headers)
    y = x.json()
    y['layer']['defaultStyle']['name'] = workspace + ':cluster_base'
    x = requests.put(url_layer, auth=('admin', 'geoserver'), headers=headers, data=str(y))
    print(x)

    # layer groups
    x = {'layerGroup': {'name': f'{i}_combined',
                        'mode': 'SINGLE',
                        'title': f'{i}_combined',
                        'publishables': {'published': [{'@type': 'layer', 'name': f'{workspace}:clustered'},
                                                       {'@type': 'layer', 'name': f'{workspace}:{i}'}]},
                        'styles': {'style': [{'name': workspace + ':cluster'},
                                             {'name': workspace + ':cluster_base'}]}}}
    x = requests.post(url_base + 'layergroups', auth=('admin', 'geoserver'), headers=headers, data=str(x))
    # clean directory
    os.system(f'del data\\{i}*')
