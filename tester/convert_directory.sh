#!/bin/bash

# Get directory to convert files in
directory=$(\
	zenity \
	--file-selection \
	--directory \
	--title="Select a directory to convert" \
)

# If none selected, quit.
if [ $? != 0 ] 
then
	exit 1
fi

# Select source encoding from a list.
source_encoding=$(\
	zenity --list \
	--column="Encoding" \
	--title="Source encoding" \
	--text="The files are currently encoded as... " \
	WINDOWS-1250 UTF-8 \
)

# If none selected, quit.
if [ $? != 0 ] 
then
	exit 1
fi

# Select destination encoding from a list.
destination_encoding=$(\
	zenity --list \
	--column="Encoding" \
	--title="Destination encoding" \
	--text="And you want these files encoded as... " \
	UTF-8 WINDOWS-1250 \
)

# If none selected, quit.
if [ $? != 0 ] 
then
	exit 1
fi 

# For all files in the selected directory...
find "$directory" -type f | while read f
do 
	# Get the necessary information.
	extension=${f#*.}
	basename=$(basename "$f" ".$extension")
	addition=$(echo "$destination_encoding" | tr -d - | tr [A-Z] [a-z])
	output="$directory/$basename.$addition.$extension"
	
	# Convert encoding.
	iconv \
		--from-code="$source_encoding" \
		--to-code="$destination_encoding" \
		--output="$output" \
		"$f"

	echo "Created $directory/$basename.$addition.$extension"
done

# Notify on finish
zenity --info --text="Operation complete." --title="Complete"

