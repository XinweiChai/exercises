#!/bin/bash
shopt -s nullglob
path=3-level
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
# 	FROM (SELECT *, ST_ClusterDBSCAN(ST_Transform(ST_SetSRID(geom, 4326), 3857), eps := 50, minpoints := 2) over () AS cid FROM '$1') cluster 
# 	WHERE cid IS NOT NULL GROUP BY cid) area WHERE sum_area>$i'"
# done
	eval "$connect -c 'CREATE TABLE $1'_'cluster AS SELECT * FROM (SELECT ROUND(sum(area)) AS sum_area,
	ST_ConcaveHull(ST_Collect(ST_Transform(ST_SetSRID(geom, 4326), 3857)), 0.99) AS geom, 
	cid, 
	count(*) as count,
	ST_X(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_x, 
	ST_Y(ST_Centroid(ST_ConcaveHull(ST_Collect(geom),0.99))) AS centroid_y 
	FROM (SELECT *, ST_ClusterDBSCAN(ST_Transform(ST_SetSRID(geom, 4326), 3857), eps := 50, minpoints := 2) over () AS cid FROM '$1') cluster 
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
	# $connect -c 'UPDATE $2 SET cat=3 WHERE cat=4'
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
	$connect -c "DROP TABLE $1'_'cluster'_'$one$two$three"
done
}
function drop(){
for i in 100 300 500
do
	eval "$connect -c 'DROP TABLE $1'_'$i'"
done
}
for province in `ls $path`
do
	flag_province=1
	for city in `ls $path/$province`
	do
		flag_city=1
		for county in `ls $path/$province/$city/*.shp`
		do
			echo county=$county
			temp=${county#$path/$province/$city/}
			name=${temp%.shp}
			# echo $province.$city'_'$name
			# upload $county $province.$city'_'$name
			# if test $flag_city -eq 1
			# then	 
			# 	upload $county $province.$city
			# 	flag_city=0
			# else
			# 	shp2pgsql -a -s 3857 $county $province.$city|$connect
			# fi
			# if test $flag_province -eq 1
			# then	 
			# 	upload $county $province.$province
			# 	flag_province=0
			# else
			# 	shp2pgsql -a -s 3857 $county $province.$province|$connect
			# fi
			# drop $province.$city'_'$name
			# cluster $province.$city'_'$name
			# drop_category $province.$city'_'$name
			cluster_category $province.$city'_'$name
		done
		# drop $province.$city
		# cluster $province.$city
		# drop_category $province.$city
		cluster_category $province.$city
	done
	# drop $province.$province
	# cluster $province.$province
	# drop_category $province.$province
	cluster_category $province.$province
done
