from pymapd import connect

con = connect(user="admin", password="HyperInteractive", host="localhost", dbname="omnisci")
c = con.cursor()
# c.execute("SELECT COUNT(*) FROM bike_part WHERE abs(lng-116.41353)<0.0001 AND abs(lat-39.859782)<0.0001")
c.execute("SELECT * FROM devices WHERE ST_DISTANCE(ST_TRANSFORM(omnisci_geo,900913),ST_TRANSFORM(ST_SETSRID('POINT(116.210709994757 33.4577449706652)', 4326),900913))<1")
x = c.fetchall()
[print(i) for i in x]
