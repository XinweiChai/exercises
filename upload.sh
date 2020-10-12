#!/bin/bash
shopt -s nullglob
path=data/test/
for province in $path*/
do
	echo province=$province
	for dir in $province*
	do
		echo dir=$dir
		for Name in $dir/*.shp
		do
			echo Name=$Name
			newName=${Name#$dir/}
			prov=${province#$path}
			echo prov=$prov
			echo ${prov%/}.${dir#$province}_${newName%.shp}
			shp2pgsql -c -s 3857 $Name ${prov%/}.${dir#$province}_${newName%.shp} > temp.sql
			PGPASSWORD=123 psql -h localhost -d postgres -U postgres -f temp.sql
		done
	done
done
