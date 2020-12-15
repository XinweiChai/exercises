import psycopg2

provinces = ["anhuisheng", "beijingshi", "fujiansheng", "guangdongsheng", "guizhousheng", "hainansheng", "heilongjiang",
             "henansheng", "hubeisheng", "hunansheng", "jiangsusheng", "jiangxisheng", "jilinsheng", "liaoningsheng",
             "shandongsheng", "shanghaishi", "shanxisheng", "shanxisheng_1", "tianjinshi", "yunnansheng",
             "zhongqingshi", "zhejiangsheng"]
cnx = psycopg2.connect(user='postgres', password='postgres', host='114.113.156.108', database='aqua', port=5432)
cur = cnx.cursor()
for i in provinces:
    cur.execute(f"SELECT count(table_name) FROM information_schema.tables WHERE table_schema = '{i}'")
    x = cur.fetchall()[0][0]
    if x % 8 != 0:
        print(i)
    # x = [i[0] for i in cur.fetchall()]
    # for table in cur.fetchall():
    #     print(table)
