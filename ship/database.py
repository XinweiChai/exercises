import pandas as pd
import psycopg2
import datetime
import random
import redis

num_side = 71
timeInterval = 10
stepLength = 0.1
lng_spacing = 2.4
lat_spacing = 1.2
iterations = 30

cnx = psycopg2.connect(user='postgres', password='postgres', host='114.113.156.108', database='ship', port=5432)
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
cursor = cnx.cursor()
curr = datetime.datetime.now().strftime('%Y-%m-%d')
# cursor.execute(f"DROP TABLE \"{curr}\"")
# cursor.execute(f"DROP TABLE current")
cursor.execute(f"CREATE TABLE IF NOT EXISTS \"{curr}\"("
               "id integer, "
               "name character varying,"
               "time timestamp without time zone,"
               "pos_x double precision,"
               "pos_y double precision,"
               "cat integer,"
               "tonnage double precision,"
               "info character varying,"
               "affiliation character varying)")
cursor.execute(f"CREATE TABLE IF NOT EXISTS current ("
               "id integer primary key, "
               "name character varying,"
               "time timestamp without time zone,"
               "pos_x double precision,"
               "pos_y double precision,"
               "cat integer,"
               "tonnage double precision,"
               "info character varying,"
               "affiliation character varying)")
# cursor.execute(f"CREATE INDEX index_time ON \"{curr}\" USING BTREE (time)")
# cursor.execute(f"CREATE INDEX index_id ON \"{curr}\" USING BTREE (id)")
# cursor.execute(f"CREATE INDEX index_time ON current USING BTREE (time)")
# cursor.execute(f"CREATE INDEX index_id ON current USING BTREE (id)")
cnx.commit()

ships = {}
for i in range(num_side):
    for j in range(num_side):
        tempi = lng_spacing * (i - num_side / 2)
        tempj = lat_spacing * (j - num_side / 2)
        id = num_side * i + j
        ships[id] = {'id': id, 'name': 'ship_' + str(id),
                     'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'pos_x': tempi, 'pos_y': tempj,
                     'cat': id % 5, 'tonnage': 60.0 + (id % 5) * 0.1, 'info': 'XXX', 'affiliation': 'XXX_fleet'}

while True:
    # for t in range(iterations):
    begin = datetime.datetime.now()
    for i in range(num_side):
        for j in range(num_side):
            id = num_side * i + j
            test = ships[id]['pos_x']
            tempi = ships[id]['pos_x'] + (random.random() - 0.5) * lng_spacing
            tempj = ships[id]['pos_y'] + (random.random() - 0.5) * lat_spacing
            content = {'id': id, 'name': 'ship_' + str(id),
                       'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'pos_x': tempi, 'pos_y': tempj,
                       'cat': id % 5, 'tonnage': ships[id]['tonnage'], 'info': 'XXX', 'affiliation': 'XXX_fleet'}
            r.hset('ship', id, str(content))
            r.lpush('ship2', str(content))
            if r.llen('ship2') > 10000:
                x = r.lrange('ship2', 0, -1)
                [i for i in x]
            # ships[id] = content
            # val = list(content.values())
            # val = [f"\'{str(i)}\'" for i in val]
            # cursor.execute(f"INSERT INTO \"{curr}\" VALUES ({','.join(val)})")
            # cursor.execute(f"INSERT INTO current VALUES ({','.join(val)}) ON CONFLICT(id) DO "
            #                f"UPDATE SET time={val[2]}, pos_x={tempi}, pos_y={tempj}")
            # cursor.execute(f"UPDATE current SET time={val[2]}, pos_x={tempi}, pos_y={tempj} WHERE id={id}")
    # cnx.commit()
    # print(f"i={i}")
    end = datetime.datetime.now()
    print(end - begin)
