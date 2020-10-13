#!/bin/bash
function read_dir(){
	for file in `ls $1`
	do
		if [ -d $1/$file ]
		then
			do_something $1/$file
			read_dir $1/$file
		fi
	done
}
function do_something(){
	# rm -f $1/*.lock
	# rm -f $1/*.xml
	# rm -f $1/*.xls
	# rm -f $1/*.xlsx
	# rm -f $1/*.jpg
	# rm -f $1/*.png
}
read_dir $1