import requests
import json
import os

workspace = 'aqua_cluster'
# db_ip = '114.113.156.108'
db_ip = '192.168.156.35'
db = 'aqua'
pw = 'postgres'
username = 'postgres'
# url_base = 'http://localhost:8080/geoserver/rest/'
url_base = 'http://192.168.156.32:8080/geoserver/rest/'

for i in os.listdir('data/3-level'):
    # path = 'E:/exercises/aquaculture/'
    path = os.getcwd()
    # get data and compress to zip
    os.system(f'pgsql2shp -f data/{i}.shp -h {db_ip} -P {pw} -u {username} {db} '
              f'\"SELECT cat,area,geom FROM {i}.{i}\"')
    os.system(f'7za a data/{i}_data.zip {path}/data/{i}.*')
    auth = ('admin', 'geoserver')
    url_store = url_base + 'workspaces/' + workspace + '/datastores/' + i + '/'

    # upload data to store
    x = requests.put(url_store + 'file.shp', auth=auth, headers={'content-type': 'application/zip'},
                     data=open(f'data/{i}_data.zip', 'rb').read())
    print(x)
    print('upload data to store')
    url_feature = url_store + 'featuretypes/' + i + '.json'
    url_layer = url_base + 'layers/' + workspace + ':' + i + '.json'
    headers = {'content-type': 'application/json'}

    # set projection of feature
    x = requests.get(url_feature, auth=auth, headers=headers)
    y = x.json()
    y['featureType']['srs'] = 'EPSG:4326'
    x = requests.put(url_feature, auth=auth, headers=headers, data=str(y))
    print(x)
    print('set feature')

    # set layer style
    x = requests.get(url_layer, auth=auth, headers=headers)
    y = x.json()
    y['layer']['defaultStyle']['name'] = workspace + ':cluster_base'
    x = requests.put(url_layer, auth=auth, headers=headers, data=str(y))
    print(x)
    print('set style')

    # create layer group
    x = {'layerGroup': {'name': f'{i}_combined',
                        'mode': 'SINGLE',
                        'title': f'{i}_combined',
                        'publishables': {'published': [{'@type': 'layer', 'name': f'{workspace}:clustered'},
                                                       {'@type': 'layer', 'name': f'{workspace}:{i}'}]},
                        'styles': {'style': [{'name': workspace + ':cluster'},
                                             {'name': workspace + ':cluster_base'}]}}}
    x = requests.post(url_base + 'layergroups', auth=auth, headers=headers, data=str(x))
    print(x)
    print('create layer groups')

    # clean directory
    os.system(f'rm data/{i}*')

