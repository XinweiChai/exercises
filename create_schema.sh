#!/bin/bash
for level in `ls data`
do
	for province in `ls data/$level`
	do
		PGPASSWORD=postgres psql -h 172.169.0.6 -d aqua -U postgres -c 'CREATE SCHEMA '$province''
	done
done