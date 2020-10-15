#!/bin/bash
shopt -s nullglob
path=data/3-level
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
			echo $province.$city'_'$name
			upload $county $province.$city'_'$name
			if test $flag_city -eq 1
			then	 
				upload $county $province.$city
				flag_city=0
			else
				shp2pgsql -a -s 3857 $county $province.$city|PGPASSWORD=postgres psql -h 172.168.2.164 -d aqua -U postgres
			fi
			if test $flag_province -eq 1
			then	 
				upload $county $province.$province
				flag_province=0
			else
				shp2pgsql -a -s 3857 $county $province.$province|PGPASSWORD=postgres psql -h 172.168.2.164 -d aqua -U postgres
			fi
	# 		for j in 100 300 500
	# 		do
	# 			# drop $province.$city'_'$name $j
	# 			cluster $province.$city'_'$name $j
	# 		done
		done
	# 	for j in 100 300 500
	# 	do
	# 		# drop $province.$city $j
	# 		cluster $province.$city $j
	# 	done
	# done
	# for j in 100 300 500
	# do
	# 	# drop $province.$province $j
	# 	cluster $province.$province $j
	done
done
