from pyproj import Proj, transform
from math import log, tan, cos, radians, degrees
import numpy as np
import pandas
from PIL import Image
import shapefile
from time import process_time
import geohash2
import pandas as pd
import os
import sys
import itertools

geohash_letters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm',
                   'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

prefix = ['wx43', 'wx46', 'wx47', 'wx4k', 'wx4m', 'wx49', 'wx4d', 'wx4e', 'wx4s', 'wx4t', 'wx4c', 'wx4f', 'wx4g',
          'wx4u', 'wx4v', 'wx51', 'wx54', 'wx55', 'wx5h', 'wx5j']


def read_csv(filename):
    file = open(filename, 'r')

    sample = [[float(val) for val in line.split(",")] for line in file if len(line.strip()) > 0]

    file.close()
    return sample


def transform_4326_proj_tiles(fn):
    fn2 = fn + "_trans"
    with open(fn2, 'w+') as f2:
        data = read_csv(fn)
        count = 0
        for i in data:
            count = count + 1
            if count % 100000 == 0:
                print(count)
            lat = degrees(log(tan(radians(i[1])) + 1 / cos(radians(i[1]))))
            f2.write("%s,%s" % (i[0], lat))
            f2.write("\n")


def transform_4326_3857(fn):
    fn2 = fn + "_3857"
    with open(fn2, 'w+') as f2:
        count = 0
        data = read_csv(fn)
        for i in data:
            count = count + 1
            x = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), i[0], i[1])
            if count % 100000 == 0:
                print(count)
            f2.write("%s,%s" % (x[0], x[1]))
            f2.write("\n")


def empty_image(fn):
    img = Image.new('RGBA', (256, 256))
    img.save(fn)


def swap_column(fn):
    t1 = process_time()
    sample = read_csv(fn)
    t2 = process_time()
    print(t2 - t1)
    with open(fn + "_swapped", "w+") as file:
        for i in sample:
            file.write("%s,%s\n" % (i[1], i[0]))
    t3 = process_time()
    print(t3 - t2)


def filter_line(fn):
    with open(fn, 'r') as file:
        with open(fn + "_filtered", "w+") as file2:
            with open(fn + "_rest", "w+") as file3:
                for line in file:
                    line = line.strip()
                    i = line.split(",")
                    if float(i[1]) < 118:
                        file2.write("%s,%s\n" % (i[0], i[1]))
                    else:
                        file3.write("%s,%s\n" % (i[0], i[1]))


def part(fn, num_lines):
    with open(fn, 'r') as file:
        with open(fn + "_%.0e" % num_lines, "w+") as file2:
            count = 0
            for line in file:
                count = count + 1
                if count > num_lines:
                    break
                file2.write(line)


def cascade(fn, nums):
    for i in nums:
        part(fn, i)


def generate_rectangles(rect, level):
    rectangles = [rect]
    for i in range(level):
        rect = [0.75 * rect[0] + 0.25 * rect[2],
                0.75 * rect[1] + 0.25 * rect[3],
                0.25 * rect[0] + 0.75 * rect[2],
                0.25 * rect[1] + 0.75 * rect[3]]
        rectangles.append(rect)
    return rectangles


def write_file(array, fn):
    with open(fn, "w+") as f:
        for i in array:
            f.write(",".join([str(j) for j in i]) + "\n")


def envelope(geohash):
    lat, lon, lat_err, lon_err = geohash2.decode_exactly(geohash)
    temp = [lat - lat_err, lat + lat_err, lon - lon_err, lon + lon_err]
    temp = [str(i) for i in temp]
    temp = ",".join(temp)
    return temp


def generate_grid():
    with open("a_big2.csv", "w") as f:
        f.write("xmini,xmaxi,ymini,ymaxi,count\n")
        for j in prefix:
            for i in itertools.product(geohash_letters, repeat=4):
                f.write(envelope(j + "".join(i)) + ",0\n")


def grid_list(directory):
    dat = pd.read_csv(directory + "y")
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            dat2 = pd.read_csv(directory + filename, dtype={"count": int})
            # x = pd.DataFrame(dat["geom"].unique(), columns=['geom'])
            # x.to_csv(dir + 'y', index=False)
            y = dat.join(dat2.set_index('envelope'), on='geom')
            y = y.fillna(0)
            y["count"] = y["count"].astype(int)
            # x.to_csv("all_variables.csv", header=False, index=False)
            y.to_csv(filename, index=False)


if __name__ == "__main__":
    # transform_4326_3857("points.csv")
    # bound = [115.87, 39.58, 116.95, 40.36]
    # bound =[]
    # x = generate_rectangles(bound, 10)
    # write_file(x, "C:/Users/Administrator/Desktop/array.csv")
    # num = [3e6, 6e6, 1e7, 5e7, 1e8, 5e8]
    # empty_image("C:/Users/Administrator/Downloads/GeoSparkTemplateProject/geospark-viz/scala/target/demo/empty.png")
    # swap_column("points.csv")
    # swap_column("C:/Users/Administrator/Desktop/b_code_stats.csv")
    # filter_line("C:/Users/Administrator/Desktop/b_code_stats.csv_swapped")
    # part("C:/Users/Administrator/Desktop/b_code_stats.csv_swapped_filtered", 500)
    # file_name = "road_dushigaosulu"
    # file = "Roadchina_Merge"
    # x = shapefile.Reader("C:/Users/Administrator/Desktop/ChinaLBS/spark/resources/res_buff/buff_res")
    # y = x.shapes()
    # z = x.records()
    # swap_column_shp(
    #     "C:/Users/Administrator/Downloads/GeoSparkTemplateProject/geospark-viz/scala/resources/roads/" + file_name + "/" + file_name)
    # take_column("C:/Users/Administrator/Desktop/ChinaLBS/Clusters_with_partition/test.csv", [1, 3])
    # grid_list(sys.argv[1])
    generate_grid()
