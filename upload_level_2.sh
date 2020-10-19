#!/bin/bash
shopt -s nullglob
path=data/2-level
connect="PGPASSWORD=postgres psql -h 172.168.2.164 -d aqua -U postgres"
function cluster(){
# for i in 100 300 500
# do
# 	PGPASSWORD=postgres psql -h 172.168.2.164 -d aqua -U postgres -c 'CREATE TABLE '$1'_'$i' AS SELECT * FROM (SELECT ROUND(sum(area)) AS sum_area,
# 	ST_ConcaveHull(ST_Collect(ST_Transform(ST_SetSRID(geom, 4326), 3857)), 0.99) AS geom, 
# 	cid, 
# 	count(*) as count,
# 	ST_X(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_x, 
# 	ST_Y(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_y 
# 	FROM (SELECT *, ST_ClusterDBSCAN(ST_Transform(ST_SetSRID(geom, 4326), 3857), eps := 50, minpoints := 2) over () AS cid FROM '$1') cluster 
# 	WHERE cid IS NOT NULL GROUP BY cid) area WHERE sum_area>'$i''
# done
	$connect -c 'CREATE TABLE '$1'_cluster AS SELECT * FROM (SELECT ROUND(sum(area)) AS sum_area,
	ST_ConcaveHull(ST_Collect(ST_Transform(ST_SetSRID(geom, 4326), 3857)), 0.99) AS geom, 
	cid, 
	count(*) as count,
	ST_X(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_x, 
	ST_Y(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_y 
	FROM (SELECT *, ST_ClusterDBSCAN(ST_Transform(ST_SetSRID(geom, 4326), 3857), eps := 50, minpoints := 2) over () AS cid FROM '$1') cluster 
	WHERE cid IS NOT NULL GROUP BY cid) area'
}
function upload(){
	shp2pgsql -c -s 4326 $1 $2|$connect
	# $connect -c 'UPDATE '$2' SET cat=3 WHERE cat=4'
}
function drop(){
for i in 100 300 500
do
	$connect -c 'DROP TABLE '$1'_'$2''
done
}
function alter(){
	$connect -c 'ALTER TABLE '$1'_'$2' ADD count integer'
	$connect -c 'UPDATE '$1'_'$2' SET count = '
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
	# 		shp2pgsql -a -s 3857 $county $city.$city|$connect
	# 	fi
		# drop $city.$name $i
		cluster $city.$name $i
	done
	# drop $city.$city $i
	cluster $city.$city $i
done