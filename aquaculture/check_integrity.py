import psycopg2

# provinces = ["anhuisheng", "beijingshi", "fujiansheng", "guangdongsheng", "guizhousheng", "hainansheng", "heilongjiang",
#              "henansheng", "hubeisheng", "hunansheng", "jiangsusheng", "jiangxisheng", "jilinsheng", "liaoningsheng",
#              "shandongsheng", "shanghaishi", "shanxisheng", "shanxisheng_1", "tianjinshi", "yunnansheng",
#              "zhongqingshi", "zhejiangsheng"]
cnx = psycopg2.connect(user='postgres', password='postgres', host='114.113.156.108', database='aqua', port=5432)
cur = cnx.cursor()
cur.execute("select schema_name from information_schema.schemata where schema_name "
            "not in ('public', 'information_schema') and schema_name not like 'pg%'")
x = cur.fetchall()
provinces = [i[0] for i in x]


def check_integrity():
    for i in provinces:
        cur.execute(f"SELECT count(table_name) FROM information_schema.tables WHERE table_schema = '{i}'")
        x = cur.fetchall()[0][0]
        if x % 8 != 1:
            print(i)
        # x = [i[0] for i in cur.fetchall()]
        # for table in cur.fetchall():
        #     print(table)


def meta_data():
    for i in provinces:
        cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{i}'")
        x = cur.fetchall()
        tables = [i[0] for i in x]
        cur.execute(f"DROP TABLE IF EXISTS {i}.meta_data")
        cur.execute(f"CREATE TABLE {i}.meta_data(place character varying, "
                    "lon_min double precision, lon_max double precision, "
                    "lat_min double precision, lat_max double precision, "
                    "centroid_x double precision, centroid_y double precision)")
        cnx.commit()
        for j in tables:
            if "cluster" not in j and j != 'meta_data':
                cur.execute(f"SELECT ST_XMIN(ST_COLLECT(geom)), "
                            f"ST_XMAX(ST_COLLECT(geom)),"
                            f"ST_YMIN(ST_COLLECT(geom)),"
                            f"ST_YMAX(ST_COLLECT(geom)),"
                            f"ST_X(ST_Centroid(ST_Collect(geom))), "
                            f"ST_Y(ST_Centroid(ST_Collect(geom)))"
                            f"FROM {i}.{j}")
                x = cur.fetchall()[0]
                cur.execute(f"INSERT INTO {i}.meta_data VALUES ('{i}_{j}',{x[0]},{x[1]},{x[2]},{x[3]},{x[4]},{x[5]})")
                cnx.commit()


if __name__ == '__main__':
    # meta_data()
    check_integrity()
