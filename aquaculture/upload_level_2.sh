#!/bin/bash
shopt -s nullglob
path=2-level
connect="PGPASSWORD=postgres psql -h 192.168.156.35 -d aqua -U postgres"
function cluster(){
# for i in 100 300 500
# do
# 	eval "$connect -c 'CREATE TABLE $1'_'$i AS SELECT * FROM (SELECT ROUND(sum(area)) AS sum_area,
# 	ST_ConcaveHull(ST_Collect(ST_Transform(ST_SetSRID(geom, 4326), 3857)), 0.99) AS geom, 
# 	cid, 
# 	count(*) as count,
# 	ST_X(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_x, 
# 	ST_Y(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_y 
# 	FROM (SELECT *, ST_ClusterDBSCAN(ST_Transform(ST_SetSRID(geom, 4326), 3857), eps := 50, minpoints := 2) over () AS cid FROM $1) cluster 
# 	WHERE cid IS NOT NULL GROUP BY cid) area WHERE sum_area>$i'"
# done
	eval "$connect -c 'CREATE TABLE $1'_'cluster AS SELECT * FROM (SELECT ROUND(sum(area)) AS sum_area,
	ST_ConcaveHull(ST_Collect(ST_Transform(ST_SetSRID(geom, 4326), 3857)), 0.99) AS geom, 
	cid, 
	count(*) as count,
	ST_X(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_x, 
	ST_Y(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_y 
	FROM (SELECT *, ST_ClusterDBSCAN(ST_Transform(ST_SetSRID(geom, 4326), 3857), eps := 50, minpoints := 2) over () AS cid FROM $1) cluster 
	WHERE cid IS NOT NULL GROUP BY cid) area'"
}

function cluster_category(){
for x in {1..6}
do
	str=''
	let one=x%2
	let x=x/2
	let two=x%2
	let x=x/2
	let three=x%2
	echo $one$two$three
	if [ $one -eq 1 ]
	then
		str=$str'cast(cat AS integer)=1 OR '
	fi
	if [ $two -eq 1 ]
	then
		str=$str'cast(cat AS integer)=2 OR '
	fi
	if [ $three -eq 1 ]
	then
		str=$str'cast(cat AS integer)>=3 OR '
	fi
	str=${str% OR }
	echo $str
	eval "$connect -c 'CREATE TABLE $1'_'cluster'_'$one$two$three AS SELECT * FROM (SELECT ROUND(sum(area)) AS sum_area,
	ST_ConcaveHull(ST_Collect(ST_Transform(ST_SetSRID(geom, 4326), 3857)), 0.99) AS geom, 
	cid, 
	count(*) as count,
	ST_X(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_x, 
	ST_Y(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_y 
	FROM (SELECT *, ST_ClusterDBSCAN(ST_Transform(ST_SetSRID(geom, 4326), 3857), eps := 50, minpoints := 2) over () AS cid FROM $1 WHERE ($str)) cluster 
	WHERE cid IS NOT NULL GROUP BY cid) area'"
done
}
function upload(){
	shp2pgsql -c -s 4326 $1 $2|$connect
	# $connect -c 'UPDATE '$2' SET cat=3 WHERE cat=4'
}
function drop(){
for i in 100 300 500
do
	eval "$connect -c 'DROP TABLE $1'_'$i'"
done
}
function drop_category(){
for x in {1..6}
do
	str=''
	let one=x%2
	let x=x/2
	let two=x%2
	let x=x/2
	let three=x%2
	echo $one$two$three
	eval "$connect -c 'DROP TABLE $1'_'cluster'_'$one$two$three'"
done
}
function alter(){
	eval "$connect -c 'ALTER TABLE $1'_'$2 ADD count integer'"
	eval "$connect -c 'UPDATE $1'_'$2 SET count = '"
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
		# drop $city.$name
		# cluster $city.$name
		cluster_category $city.$name
		# drop_category $city.$name
	done
	# drop $city.$city
	# cluster $city.$city
	cluster_category $city.$city
	# drop_category $city.$city
done
