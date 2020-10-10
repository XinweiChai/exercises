#!/bin/bash
shopt -s nullglob
for province in */
do
	for dir in $province*/
	do
		for file in $dir*
		do
			mv $file `echo $file|sed 's/_fish//g'`
		done
	done
done