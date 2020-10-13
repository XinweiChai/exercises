#!/bin/bash
for level in `ls data`
do
	for province in `ls data/$level`
	do
		PGPASSWORD=123 psql -h localhost -d postgres -U postgres -c 'CREATE SCHEMA '$province''
	done
done