#!/bin/bash
shopt -s nullglob
path=data/2-level
function cluster(){
	PGPASSWORD=postgres psql -h 172.168.2.164 -d aqua -U postgres -c 'CREATE TABLE '$1'_'$2' AS SELECT * FROM (SELECT ROUND(sum(area)) AS sum_area,
	 ST_ConcaveHull(ST_Collect(ST_Transform(ST_SetSRID(geom, 4326), 3857)), 0.99) AS geom, 
	 cid, 
	 count(*) as count,
	 ST_X(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_x, 
	 ST_Y(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_y 
	 FROM (SELECT *, ST_ClusterDBSCAN(ST_Transform(ST_SetSRID(geom, 4326), 3857), eps := 50, minpoints := 2) over () AS cid FROM '$1') cluster 
	 WHERE cid IS NOT NULL GROUP BY cid) area WHERE sum_area>'$2''
}
function upload(){
	shp2pgsql -c -s 3857 $1 $2|PGPASSWORD=postgres psql -h 172.168.2.164 -d aqua -U postgres
	# PGPASSWORD=postgres psql -h 172.168.2.164 -d aqua -U postgres -c 'UPDATE '$2' SET cat=3 WHERE cat=4'
}
function drop(){
	PGPASSWORD=postgres psql -h 172.168.2.164 -d aqua -U postgres -c 'DROP TABLE '$1'_'$2''
}
function alter(){
	PGPASSWORD=postgres psql -h 172.168.2.164 -d aqua -U postgres -c 'ALTER TABLE '$1'_'$2' ADD count integer'
	PGPASSWORD=postgres psql -h 172.168.2.164 -d aqua -U postgres -c 'UPDATE '$1'_'$2' SET count = '
}
for city in `ls $path`
do
	flag=1
	echo city=$city
	for county in `ls $path/$city/*.shp`
	do
		echo county=$county
		temp=${county#$path/$city/}
		name=${temp%.shp}
		echo $city.$name
	# 	upload $county $city.$name
	# 	if test $flag -eq 1
	# 	then	 
	# 		upload $county $city.$city
	# 		flag=0
	# 	else
	# 		shp2pgsql -a -s 3857 $county $city.$city|PGPASSWORD=postgres psql -h 172.168.2.164 -d aqua -U postgres
	# 	fi
		for i in 100 300 500
		do
			drop $city.$name $i
			cluster $city.$name $i
		done
	done
	for i in 100 300 500
	do
		drop $city.$city $i
		cluster $city.$city $i
	done
done