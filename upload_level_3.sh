#!/bin/bash
shopt -s nullglob
path=data/3-level
function cluster(){
	PGPASSWORD=123 psql -h localhost -d postgres -U postgres -c 'CREATE TABLE '$1'_'$2' AS SELECT * FROM (SELECT ROUND(sum(area)) AS sum_area, ST_ConcaveHull(ST_Collect(ST_Transform(ST_SetSRID(geom, 4326), 3857)), 0.99) AS geom, cid FROM (SELECT *, ST_ClusterDBSCAN(ST_Transform(ST_SetSRID(geom, 4326), 3857), eps := 50, minpoints := 2) over () AS cid FROM '$1') cluster WHERE cid IS NOT NULL GROUP BY cid) area WHERE sum_area>'$2''
}
function upload(){
	shp2pgsql -c -s 3857 $1 $2|PGPASSWORD=123 psql -h localhost -d postgres -U postgres
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
				shp2pgsql -a -s 3857 $county $province.$city|PGPASSWORD=123 psql -h localhost -d postgres -U postgres
			fi
			if test $flag_province -eq 1
			then	 
				upload $county $province.$province
				flag_province=0
			else
				shp2pgsql -a -s 3857 $county $province.$province|PGPASSWORD=123 psql -h localhost -d postgres -U postgres
			fi
				for j in 100 300 500
				do
					cluster $province.$city'_'$county $j
				done
		done
		for j in 100 300 500
		do
			cluster $province.$city $j
		done
	done
	for j in 100 300 500
	do
		cluster $province.$province $j
	done
done
