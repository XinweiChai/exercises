#!/bin/bash
shopt -s nullglob
for province in */
do
	for dir in $province*
	do
		echo $dir
		for Name in $dir/*.shp
		do
			echo $Name
			newName=${Name#$dir/}
			#echo ${province%/}.${dir#$province}_${newName%.shp}
			shp2pgsql -c -s 3857 $Name ${province%/}.${dir#$province}_${newName%.shp} > temp.sql
			PGPASSWORD=123 psql -h localhost -d postgres -U postgres -f temp.sql
		done
	done
done
