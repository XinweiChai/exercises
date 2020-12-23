import requests
import os
import psycopg2

workspace = 'aqua_cluster'
# db_ip = '172.168.2.164'
db_ip = '192.168.156.35'
db = 'aqua'
pw = 'postgres'
username = 'postgres'
# url_base = 'http://localhost:8080/geoserver/'
# url_base = 'http://172.169.0.6:8080/geoserver/'
url_base = 'http://192.168.156.32:8080/geoserver/'
# auth = ('admin', 'geoserver')
auth = ('xw.chai', 'chai@123.com')
headers = {'content-type': 'application/json'}
thresholds = ['100', '300', '500']

cnx = psycopg2.connect(user='postgres', password='postgres', host=db_ip, database='aqua', port=5432)
cur = cnx.cursor()
cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name "
            "not in ('public', 'information_schema') AND schema_name not like 'pg%'")
provinces = [i[0] for i in cur.fetchall()]
# provinces = ['beijingshi']


def get_tables(schema):
    cur.execute(f"SELECT tablename FROM pg_tables WHERE schemaname = '{schema}'")
    tables = [i[0] for i in cur.fetchall()]
    return tables


def compress(fn):
    path = os.getcwd()
    os.system(f'7za a data/{fn}.zip -bsp0 -bso0 {path}/data/{fn}.* -x!*.zip')


def upload(fn):
    url_store = url_base + f'rest/workspaces/{workspace}/datastores/{fn}/'
    x = requests.put(url_store + 'file.shp', auth=auth, headers={'content-type': 'application/zip'},
                     data=open(f'data/{fn}.zip', 'rb').read())
    print(x)
    print('upload data to store')
    # clean directory
    os.system(f'rm data/{fn}.*')


def set_projection(fn):
    url_store = url_base + f'rest/workspaces/{workspace}/datastores/{fn}/'
    url_feature = url_store + f'featuretypes/{fn}.json'
    x = requests.get(url_feature, auth=auth, headers=headers)
    y = x.json()
    y['featureType']['srs'] = 'EPSG:4326'
    x = requests.put(url_feature, auth=auth, headers=headers, data=str(y))
    print(x)
    print('set feature')


def set_style(fn, cat):
    url_layer = url_base + f'rest/layers/{workspace}:{fn}.json'
    x = requests.get(url_layer, auth=auth, headers=headers)
    y = x.json()
    y['layer']['defaultStyle']['name'] = f'{workspace}:{cat}'
    x = requests.put(url_layer, auth=auth, headers=headers, data=str(y))
    print(x)
    print('set style')


def non_empty_layer(i, j, k):
    cur.execute(f"SELECT COUNT(*) FROM {i}.{j} WHERE sum_area > {k}")
    return cur.fetchall()[0][0]


def download(fn, i, j, k, cluster):
    flag = True
    if cluster:
        get_command = f'\"SELECT CAST(sum_area AS INTEGER), ST_Transform(ST_SetSRID(geom, 3857), 4326)' \
                      f' as geom FROM {i}.{j} WHERE sum_area > {k}\"'
        flag = non_empty_layer(i, j, k)
    else:
        get_command = f'\"SELECT cat,area,geom FROM {i}.{j}\"'
    if flag:
        os.system(f'pgsql2shp -f data/{fn}.shp -h {db_ip} -P {pw} -u {username} {db} ' + get_command)
        return True
    else:
        return False


def publish(fn):
    compress(fn)
    upload(fn)
    set_projection(fn)


def publish_all():
    for i in provinces:
        tables = get_tables(i)
        for j in tables:
            print(f'\n{i}:{j}')
            k = None
            if 'cluster' in j:
                for k in thresholds:
                    fn = f'{i}_{j}_{k}mu'
                    if not download(fn, i, j, k, cluster=True):
                        break
                    publish(fn)
                    set_style(fn, 'cluster_raster')
            else:
                fn = f'{i}_{j}'
                if not download(fn, i, j, k, cluster=False):
                    break
                publish(fn)
                set_style(fn, 'cluster_base')


def layer_group_json(i, j, k, fn):
    temp = j.split("_")
    json = {'layerGroup': {'name': f'{fn}_group',
                           'mode': 'SINGLE',
                           'title': f'{fn}_group',
                           'workspace': workspace,
                           'publishables': {'published': [{'@type': 'layer', 'name': f'{workspace}:{fn}'},
                                                          {'@type': 'layer', 'name': f'{workspace}:{i}_{temp[0]}'}]},
                           'styles': {'style': [{'name': f'{workspace}:cluster_raster'},
                                                {'name': f'{workspace}:cluster_base'}]}}}
    if not non_empty_layer(i, j, k):
        json['layerGroup']['publishables']['published'].pop(0)
        json['layerGroup']['styles']['style'].pop(0)
    return json


def seed_json(fn):
    return {'seedRequest': {'name': f'{fn}_group',
                            # 'bounds': {'coords': {
                            #     'double': ['-180.0', '180.0', '0', '90.0']
                            # }},
                            'srs': {'number': 4326},
                            'zoomStart': 5,
                            'zoomStop': 12,
                            'format': 'image/png',
                            'type': 'reseed',
                            'threadCount': 4
                            }
            }


def group_and_seed():
    for i in provinces:
        tables = get_tables(i)
        for j in tables:
            if "cluster" in j:
                for k in thresholds:
                    fn = f'{i}_{j}_{k}mu'
                    x = requests.post(url_base + 'rest/layergroups', auth=auth, headers=headers,
                                      data=str(layer_group_json(i, j, k, fn)))
                    print(x)
                    print('create layer group')

                    x = requests.post(f'{url_base}gwc/rest/seed/{workspace}:{fn}_group.json', auth=auth,
                                      headers=headers,
                                      data=str(seed_json(fn)))
                    print(x)
                    print('seed group')


def clean_group(fn):
    url_layer_group = url_base + f'rest/layergroups/{workspace}:{fn}' + '_group'
    x = requests.delete(url_layer_group, auth=auth)
    print(x)


def clean_layer(fn):
    url_layer = url_base + f'rest/layers/{workspace}:{fn}'
    x = requests.delete(url_layer, auth=auth)
    print(x)


def clean_store(fn):
    url_store = url_base + f'rest/workspaces/{workspace}/datastores/{fn}'
    x = requests.delete(url_store, auth=auth, params={'recurse':'true'})
    print(x)


def clean():
    for i in provinces:
        tables = get_tables(i)
        tables.reverse()
        for j in tables:
            if "cluster" in j:
                for k in thresholds:
                    if non_empty_layer(i, j, k):
                        fn = f'{i}_{j}_{k}mu'
                        clean_group(fn)
                        clean_layer(fn)
                        clean_store(fn)
            else:
                fn = f'{i}_{j}'
                clean_layer(fn)
                clean_store(fn)


if __name__ == '__main__':
    # clean()
    publish_all()
    group_and_seed()

