import requests
import json
from xml.dom.minidom import parse
import os

workspace = 'aquaculture'

for i in os.listdir("data/2-level"):
    path = 'E:/exercises/aquaculture/'
    os.system(f"pgsql2shp -f data/{i}_cluster.shp -h 172.168.2.164 -P postgres -u postgres aqua "
              f"\"SELECT CAST(sum_area AS Integer) AS sum_area, geom FROM {i}.{i}_cluster\"")
    # x = f"7z a data/{i}_cluster.zip {path}data/{i}_cluster.*"
    os.system(f"7z a data/{i}_cluster.zip {path}data/{i}_cluster.*")
    auth = ('admin', 'geoserver')
    url_base = 'http://localhost:8080/geoserver/rest/'
    url_store = url_base + 'workspaces/aquaculture/datastores/' + i + '_cluster/'
    # x = requests.put(url_store + 'file.shp', auth=auth, headers={"content-type": "application/zip"},
    #                  file=file('data/' + i + '_cluster.zip', 'rb'))
    os.system("curl -v -u admin:geoserver -XPUT -H 'content-type: application/zip' --data-binary "
              f"@data/{i}.zip {url_store}file.shp")
    url_feature = url_store + 'featuretypes/' + i + '_cluster.json'
    url_layer = url_base + 'layers/' + 'aquaculture:' + i + '_cluster.json'
    headers = {'content-type': 'application/json'}

    x = requests.get(url_feature, auth=auth, headers=headers)
    y = x.json()
    y['featureType']['srs'] = 'EPSG:3857'
    x = requests.put(url_feature, auth=auth, headers=headers, data=str(y))
    print(x)

    x = requests.get(url_layer, auth=auth, headers=headers)
    y = x.json()
    y['layer']['defaultStyle']['name'] = 'aquaculture:static_cluster'
    x = requests.put(url_layer, auth=('admin', 'geoserver'), headers=headers, data=str(y))
    print(x)
