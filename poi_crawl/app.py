from urllib.parse import quote
from urllib import request
import json
import os
import xlwt
import pandas as pd
from transCoordinateSystem import gcj02_to_wgs84, gcj02_to_bd09
from shp import trans_point_to_shp
from manip_poi_code import poi_list

'''
版本更新说明：

2019.10.05：
    1. 数据导出格式支持CSV格式以及XLS两种格式;
    2. 支持同时采集多个城市的POI数据;
    3. 支持同时采集多个POI分类数据
    
2019.10.10:
    1. 数据导出支持CSV以及XLS两种格式;
    2. CSV格式数据会生成.shp文件，可以直接在ARCGIS中使用
    
    
'''

# TODO 1.替换为上面申请的密钥
amap_web_key = '2da311fe5bbc69e2ef1550cb329c2a2f'

# TODO 2.分类关键字,最好对照<<高德地图POI分类关键字以及编码.xlsx>>来填写对应编码，多个用逗号隔开
# keyword = ['021301']
# keyword = poi_list()

# keyword = ['030201', '030202', '030203', '030204', '030205', '030206', '030301', '030302', '030303', '030401', '030501',
#            '030502', '030503', '030504', '030505', '030506', '030507', '030508', '030701', '030702', '030801', '030802',
#            '030803', '030900', '031004', '031005', '031101', '031102', '031103', '031104', '031200', '031301', '031302',
#            '031303', '031401', '031501', '031601', '031701', '031702', '031801', '031802', '031902', '031903', '031904',
#            '032000', '032100', '032200', '032300', '032401', '032500', '032601', '032602', '032700', '032800', '032900',
#            '033000', '033100', '033200', '033300', '033401', '033500', '033600', '035000', '035100', '035200', '035300',
#            '035400', '035500', '035600', '035700', '035800', '035900', '036000', '036100', '036200', '036300', '039900',
#            '040101', '040201', '050101', '050102', '050103', '050104', '050105', '050106', '050107', '050108', '050109',
#            '050110', '050111', '050112', '050113', '050114', '050115', '050116', '050117', '050118', '050119', '050120',
#            '050121', '050122', '050123', '050201', '050202', '050203', '050204', '050205', '050206', '050207', '050208',
#            '050209', '050210', '050211', '050212', '050213', '050214', '050215', '050216', '050217', '050301', '050302',
#            '050303', '050304', '050305', '050306', '050307', '050308', '050309', '050310', '050311', '050400', '050501',
#            '050502', '050503', '050504', '050600', '050700', '050800', '050900', '060101', '060102', '060103', '060201',
#            '060202', '060301', '060302', '060303', '060304', '060305', '060306', '060307', '060308', '060401', '060402',
#            '060403', '060404', '060405', '060406', '060407', '060408', '060409', '060411', '060413', '060414', '060415',
#            '060501', '060502', '060601', '060602', '060603', '060604', '060605', '060606', '060701', '060702', '060703',
#            '060704', '060705', '060706', '060800', '060901', '060902', '060903', '060904', '060905', '060906', '060907',
#            '061001', '061101', '061102', '061103', '061104', '061201', '061202', '061203', '061204', '061205', '061206',
#            '061207', '061208', '061209', '061210', '061211', '061212', '061213', '061214', '061301', '061302', '061401',
#            '070100', '070201', '070202', '070203', '070301', '070302', '070303', '070304', '070305', '070306', '070401',
#            '070501', '070601', '070603', '070604', '070605', '070606', '070607', '070608', '070609', '070610', '070701',
#            '070702', '070703', '070704', '070705', '070706', '070800', '070900', '071000', '071100', '071200', '071300',
#            '071400', '071500', '071600', '071700', '071801', '071901', '071902', '071903', '072001', '080101', '080102',
#            '080103', '080104', '080105', '080106', '080107', '080108', '080109', '080110', '080111', '080112', '080113',
#            '080114', '080115', '080116', '080117', '080118', '080119', '080201', '080202', '080301', '080302', '080303',
#            '080304', '080305', '080306', '080307', '080308', '080401', '080402', '080501', '080502', '080503', '080504',
#            '080505', '080601', '080602', '080603', '090101', '090102', '090201', '090202', '090203', '090204', '090205',
#            '090206', '090207', '090208', '090209', '090210', '090211', '090300', '090400', '090500', '090601', '090602',
#            '090701', '090702', '100101', '100102', '100103', '100104', '100105', '100201', '110101', '110102', '110103',
#            '110104', '110105', '110106', '110201', '110202', '110203', '110204', '110205', '110206', '110207', '110208',
#            '110209', '120100', '120201', '120202', '120203', '120301', '120302', '120303', '120304', '130101', '130102',
#            '130103', '130104', '130105', '130106', '130107', '130201', '130202', '130300', '130401', '130402', '130403',
#            '130404', '130405', '130406', '130407', '130408', '130409', '130501', '130502', '130503', '130504', '130505',
#            '130506', '130601', '130602', '130603', '130604', '130605', '130606', '130701', '130702', '130703', '140101',
#            '140102', '140201', '140300', '140400', '140500', '140600', '140700', '140800', '140900', '141000', '141101',
#            '141102', '141103', '141104', '141105', '141201', '141202', '141203', '141204', '141205', '141206', '141207',
#            '141300', '141400', '141500', '150101', '150102', '150104', '150105', '150106', '150107', '150201', '150202',
#            '150203', '150204', '150205', '150206', '150207', '150208', '150209', '150210', '150301', '150302', '150303',
#            '150304', '150400', '150501', '150600', '150701', '150702', '150703', '150800', '150903', '150904', '150905',
#            '150906', '150907', '150908', '150909', '151000', '151100', '151200', '151300', '160101', '160102', '160103',
#            '160104', '160105', '160106', '160107', '160108', '160109', '160110', '160111', '160112', '160113', '160114',
#            '160115', '160117', '160118', '160119', '160120', '160121', '160122', '160123', '160124', '160125', '160126',
#            '160127', '160128', '160129', '160130', '160131', '160132', '160133', '160134', '160135', '160136', '160137',
#            '160138', '160139', '160140', '160141', '160142', '160143', '160144', '160145', '160146', '160147', '160148',
#            '160149', '160150', '160151', '160152', '160200', '160301', '160302', '160303', '160304', '160305', '160306',
#            '160307', '160308', '160309', '160310', '160311', '160312', '160314', '160315', '160316', '160317', '160318',
#            '160319', '160320', '160321', '160322', '160323', '160324', '160325', '160326', '160327', '160328', '160329',
#            '160330', '160331', '160332', '160333', '160334', '160335', '160336', '160337', '160338', '160339', '160340',
#            '160341', '160342', '160343', '160344', '160345', '160346', '160347', '160348', '160349', '160401', '160402',
#            '160403', '160404', '160405', '160406', '160407', '160408', '160501', '160600', '170100', '170201', '170202',
#            '170203', '170204', '170205', '170206', '170207', '170208', '170209', '170300', '170401', '170402', '170403',
#            '170404', '170405', '170406', '170407', '170408', '180101', '180102', '180103', '180104', '180201', '180202',
#            '180203', '180301', '180302', '180400', '180500', '190101', '190102', '190103', '190104', '190105', '190106',
#            '190107', '190108', '190109', '190201', '190202', '190203', '190204', '190205', '190301', '190302', '190303',
#            '190304', '190305', '190306', '190307', '190308', '190309', '190310', '190311', '190401', '190402', '190403',
#            '190500', '190600', '190700', '200100', '200200', '200301', '200302', '200303', '200304', '200400', '220101',
#            '220102', '220103', '220104', '220105', '220106', '220107', '220201', '220202', '220203', '220204', '220205',
#            '991001', '991401', '991500']


with open('poi_code', 'r') as f:
    keyword = f.read().split(',')

# TODO 3.城市，多个用逗号隔开
city = ['郑州市']

# TODO 4.输出数据坐标系,1为高德GCJ20坐标系，2WGS84坐标系，3百度BD09坐标系
coord = 2

# TODO 5. 输出数据文件格式,1为默认xls格式，2为csv格式
data_file_format = 2

poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"

poi_xingzheng_distrinct_url = "https://restapi.amap.com/v3/config/district?subdistrict=1&key=515d118ceea3b648f42b55096e7023c5"

count = 0


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i)
        print(result)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
            break

        hand(poilist, result)
        i = i + 1
    return poilist


# 数据写入excel
def write_to_excel(poilist, cityname, classfield):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)

    # 第一行(列标题)
    sheet.write(0, 0, 'lon')
    sheet.write(0, 1, 'lat')
    sheet.write(0, 2, 'name')
    sheet.write(0, 3, 'address')
    sheet.write(0, 4, 'pname')
    sheet.write(0, 5, 'cityname')
    sheet.write(0, 6, 'business_area')
    sheet.write(0, 7, 'type')

    for i in poilist:
        location = i['location']
        name = i['name']
        address = i['address']
        pname = i['pname']
        cityname = i['cityname']
        business_area = i['business_area']
        type = i['type']
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]

        if coord == 2:
            result = gcj02_to_wgs84(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        if coord == 3:
            result = gcj02_to_bd09(float(lng), float(lat))
            lng = result[0]
            lat = result[1]

        # 每一行写入
        sheet.write(i + 1, 0, lng)
        sheet.write(i + 1, 1, lat)
        sheet.write(i + 1, 2, name)
        sheet.write(i + 1, 3, address)
        sheet.write(i + 1, 4, pname)
        sheet.write(i + 1, 5, cityname)
        sheet.write(i + 1, 6, business_area)
        sheet.write(i + 1, 7, type)

    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'data' + os.sep + 'poi-' + cityname + "-" + classfield + ".xls")


# 数据写入csv文件中
def write_to_csv(poilist, cityname, classfield):
    data_csv = {}
    lons, lats, names, addresss, pnames, citynames, business_areas, types = [], [], [], [], [], [], [], []

    for i in poilist:
        location = i['location']
        name = i['name']
        address = i['address'] if 'address' in i.keys() else ""
        pname = i['pname']
        cityname = i['cityname']
        business_area = i['business_area']
        type = i['type']
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]

        if coord == 2:
            result = gcj02_to_wgs84(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        if coord == 3:
            result = gcj02_to_bd09(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        lons.append(lng)
        lats.append(lat)
        names.append(name)
        addresss.append(address)
        pnames.append(pname)
        citynames.append(cityname)
        if not business_area:
            business_area = ''
        business_areas.append(business_area)
        types.append(type)
    data_csv['lat'], data_csv['lon'], data_csv['name'], data_csv['address'], data_csv['pname'], \
    data_csv['cityname'], data_csv['business_area'], data_csv['type'] = \
        lats, lons, names, addresss, pnames, citynames, business_areas, types

    df = pd.DataFrame(data_csv)

    folder_name = 'poi-' + cityname + "-" + classfield
    folder_name_full = 'data' + os.sep + folder_name + os.sep
    if os.path.exists(folder_name_full) is False:
        os.makedirs(folder_name_full)

    file_name = 'poi-' + cityname + "-" + classfield + ".csv"
    file_path = folder_name_full + file_name

    df.to_csv(file_path, index=False, encoding='utf-8')
    return folder_name_full, file_name


# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in pois:
        poilist.append(i)


# 单页获取pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&types=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    global count
    count += 1
    return data


def get_areas(code):
    '''
    获取城市的所有区域
    :param code:
    :return:
    '''

    print('获取城市的所有区域：code: ' + str(code).strip())
    data = get_distrinctNoCache(code)

    print('get_distrinct result:' + data)

    data = json.loads(data)

    districts = data['districts'][0]['districts']
    # 判断是否是直辖市
    # 北京市、上海市、天津市、重庆市。
    if (code.startswith('重庆') or code.startswith('上海') or code.startswith('北京') or code.startswith('天津')):
        districts = data['districts'][0]['districts'][0]['districts']

    i = 0
    area = ""
    for district in districts:
        name = district['name']
        adcode = district['adcode']
        i = i + 1
        area = area + "," + adcode

    print(area)
    print(str(area).strip(','))
    return str(area).strip(',')


def get_data(city, keyword):
    '''
    根据城市名以及POI类型爬取数据
    :param city:
    :param keyword:
    :return:
    '''
    isNeedAreas = True
    if isNeedAreas:
        area = get_areas(city)
    all_pois = []
    if area:
        area_list = str(area).split(",")
        if area_list == 0:
            area_list = str(area).split("，")

        for area in area_list:
            pois_area = getpois(area, keyword)
            if len(pois_area) > 880:
                with open('too_many_pois', 'a+') as f:
                    f.write('当前城区：' + str(area) + ', 分类：' + str(keyword) + ", 总的有" + str(len(pois_area)) + "条数据")
            print('当前城区：' + str(area) + ', 分类：' + str(keyword) + ", 总的有" + str(len(pois_area)) + "条数据")
            all_pois.extend(pois_area)
        print("所有城区的数据汇总，总数为：" + str(len(all_pois)))
        if data_file_format == 2:
            # 写入CSV
            file_folder, file_name = write_to_csv(all_pois, city, keyword)
            # 写入SHP
            trans_point_to_shp(file_folder, file_name, 0, 1)
            return
        return write_to_excel(all_pois, city, keyword)
    else:
        pois_area = getpois(area, keyword)
        if data_file_format == 2:
            # 写入CSV
            file_folder, file_name = write_to_csv(all_pois, city, keyword)
            # 写入SHP
            trans_point_to_shp(file_folder, file_name, 0, 1)
            return
        return write_to_excel(pois_area, city, keyword)


def get_distrinctNoCache(code):
    '''
    获取中国城市行政区划
    :return:
    '''

    url = "https://restapi.amap.com/v3/config/district?subdistrict=2&extensions=all&"

    req_url = url + "&key=" + amap_web_key + "&keywords=" + quote(code)

    print(req_url)

    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    print(code, data)
    return data


if __name__ == '__main__':
    queries = keyword.copy()
    for ct in city:
        for poi_type in keyword:
            print("total queries", count)
            if count < 1800:
                get_data(ct, poi_type)
                queries.remove(poi_type)
            else:
                print("Total exceeded")
                break
    with open('poi_code', 'w') as f:
        f.write(','.join(queries))
    print("total queries", count)
    print('总的', len(city), '个城市, ', len(keyword), '个分类数据全部爬取完成!')
