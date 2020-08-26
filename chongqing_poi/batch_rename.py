import codecs
import csv
import os
import re
import shapefile as shp
import shutil
import pandas as pd


def rename():
    for folder in os.listdir("data"):
        for filename in os.listdir("data/" + folder):
            x = re.split(r'\.', filename)
            x[0] = folder
            x = '.'.join(x)
            os.rename("data/" + folder + '/' + filename, "data/" + folder + '/' + x)


def trans_point_to_shp(folder, fn, idlng, idlat, delimiter=','):
    w = shp.Writer(folder + fn, encoding='utf-8')
    w.field('lon', 'F', 10, 8)
    w.field('lat', 'F', 10, 8)
    w.field('name', 'C', 100)
    w.field('address', 'C', 100)
    w.field('pname', 'C', 10, 8)  # float
    w.field('cityname', 'C', 10, 8)  # float
    w.field('business_area', 'C', 100)  # string, max-length
    w.field('type', 'C', 100)  # string, max-length
    with codecs.open(folder + fn, 'rb', 'utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        # skip the header
        next(reader, None)
        # loop through each of the rows and assign the attributes to variables
        for row in reader:
            name = row[2]
            address = row[3]
            pname = row[4]
            cityname = row[5]
            business_area = row[6]
            type = row[7]
            lng = float(row[idlng])
            lat = float(row[idlat])
            w.point(lng, lat)
            w.record(lng, lat, name, address, pname, cityname, business_area, type)
    w.close()


def batch_transfer():
    for folder in os.listdir("data"):
        for filename in os.listdir("data/" + folder):
            x = re.split(r'\.', filename)
            if x[1] == 'csv':
                trans_point_to_shp('data/' + folder + '/', filename, 1, 0, delimiter=',')
                break


def regroup():
    prefix = 'poi-重庆市-'
    for folder in os.listdir("data"):
        if prefix in folder:
            code = folder[8:]
            if not os.path.isdir('data/' + code[0:2]):
                os.mkdir('data/' + code[0:2])
            shutil.move('data/' + folder, 'data/' + code[0:2])


def combine():
    for folder in os.listdir('data/'):
        w = shp.Writer('data/' + folder + '/' + folder, encoding='utf-8')
        w.field('lon', 'F', 10, 8)
        w.field('lat', 'F', 10, 8)
        w.field('name', 'C', 100)
        w.field('address', 'C', 100)
        w.field('pname', 'C', 0, 8)  # float
        w.field('cityname', 'C', 10, 8)  # float
        w.field('business_area', 'C', 100)  # string, max-length
        w.field('type', 'C', 100)  # string, max-length
        for subfolder in os.listdir('data/' + folder):
            if '.' not in subfolder:
                x = pd.read_csv('data/' + folder + '/' + subfolder + '/' + subfolder + '.csv')
                for index, row in x.iterrows():
                    name = row['name']
                    address = row['address']
                    pname = row['pname']
                    cityname = row['cityname']
                    business_area = row['business_area']
                    type = row['type']
                    lng = row['lon']
                    lat = row['lat']
                    w.point(lng, lat)
                    w.record(lng, lat, name, address, pname, cityname, business_area, type)
        w.close()


if __name__ == '__main__':
    # rename()
    # regroup()
    combine()
