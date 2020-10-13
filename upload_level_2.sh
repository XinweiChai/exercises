#!/bin/bash
shopt -s nullglob
path=data/2-level
function cluster(){
	PGPASSWORD=123 psql -h localhost -d postgres -U postgres -c 'CREATE TABLE '$1'_'$2' AS SELECT * FROM (SELECT ROUND(sum(area)) AS sum_area, ST_ConcaveHull(ST_Collect(ST_Transform(ST_SetSRID(geom, 4326), 3857)), 0.99) AS geom, cid FROM (SELECT *, ST_ClusterDBSCAN(ST_Transform(ST_SetSRID(geom, 4326), 3857), eps := 50, minpoints := 2) over () AS cid FROM '$1') cluster WHERE cid IS NOT NULL GROUP BY cid) area WHERE sum_area>'$2''
}
function upload(){
	shp2pgsql -c -s 3857 $1 $2|PGPASSWORD=123 psql -h localhost -d postgres -U postgres
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
		# upload $county $city.$name
		# if test $flag -eq 1
		# then	 
		# 	upload $county $city.$city
		# 	flag=0
		# else
		# 	shp2pgsql -a -s 3857 $county $city.$city|PGPASSWORD=123 psql -h localhost -d postgres -U postgres
		# fi
		for i in 100 300 500
		do
			cluster $city.$name $i
		done
	done
	for i in 100 300 500
	do
		cluster $city.$city $i
	done
done
