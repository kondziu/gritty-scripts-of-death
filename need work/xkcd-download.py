#!/usr/bin/python
#
# Requires:
# 	xml2dom (http://www.boddie.org.uk/python/libxml2dom.html)

import os
import re
import sys
import urllib
import libxml2
import urlparse
import Image			# PIL
import ImageDraw		# PIL

from htmlentitydefs import entitydefs
from xml.sax.handler import ContentHandler, EntityResolver


# Global constants
output_dir = 'downloaded'
text_extension = '.txt'
inscribe = True
verbose = True
number_files = True
cutoff = 0
offset = 0

comics = {
	'xkcd': (
		'http://xkcd.com/archive/',		# 0: Link to archive
		'UTF-8', 						# 1: Page encoding
		'//a/@href', 					# 2: XPath expression or the links
		'^/[0-9]+/$', 					# 3: Regex for the links
		'http://xkcd.com',				# 4: Prefix to the links
		'//div[@class="s"]/img',		# 5: XPath to the image
		'src',							# 6: Image attribute - link
		'title'							# 7: Image attribute - description
	)
}

# Global variables

def get_image (link, encoding, xpath, source, description):
	
	document = libxml2.htmlParseFile(link, encoding)
	context = document.xpathNewContext()
	images = context.xpathEval(xpath)
	output = []
	
	for image in images:
		output.append((image.prop(source), image.prop(description)));
	
	document.freeDoc()
	context.xpathFreeContext()
		
	return output
	
def parse_archive_by_name (name):
	return parse_archive(comics[name])

def parse_archive (comic):	
	global image_number

	if verbose:
		sys.stderr.write("Parsing archive directory: " + comic[0] + "\n")

	document = libxml2.htmlParseFile(comic[0], comic[1])
	context = document.xpathNewContext()
	anchors = context.xpathEval(comic[2])
	pattern = re.compile(comic[3])
	output = []
	
	anchors = anchors[offset:]
	image_number += offset

	for anchor in anchors:
		address = anchor.get_content()
		if pattern.match(address):
			if verbose:
				sys.stderr.write("Parsing link " + address + "\n")
			image_number += 1
			path = comic[4] + address
			pair = get_image (path, comic[1], comic[5], comic[6], comic[7])
			output.extend(pair)
			if image_number >= cutoff and cutoff > 0:
				break
			
	document.freeDoc()
	context.xpathFreeContext()
	
	return output
	
def mktextfile(filename, content):
	file_descriptor = open(filename,'w')
	file_descriptor.write(content)
	file_descriptor.close()
	
def inscribe(input, description, output):
	image = Image.open(input)
	draw = ImageDraw.Draw(image)
	size = draw.textsize(description)
	pixels_per_character = size[0] / len(description)
	max_width = image.size[0] - 2 * 5 # Two five-pixel margins.
	max_characters = max_width / pixels_per_character + 1 # 1 extra for spaces.
	
	# Prepare text
	line = 0
	prepared = []
	current = ''
	for word in description.split():
		word += ' '
		length = len(word)
		if line + length <= max_characters:
			line += length	
			current += word
		else:
			line = len(word)
			prepared.append(current)
			current = word
			#if length > max_characters:	
	if line > 0:
		prepared.append(current)
	lines = len(prepared)
	print prepared
	
	# Extend and insert text
	frame_size = (image.size[0], image.size[1] + lines * size[1] + 2 * 5) # 5px margins
	frame = Image.new(image.mode, frame_size)
	draw = ImageDraw.Draw(frame)
	for i in range(0, lines):
		print (5, image.size[1] + 5 + size[1] * i), prepared[i]
		draw.text((5, image.size[1] + 5 + size[1] * i), prepared[i], fill=0xffffff)
	frame.paste(image, (0, 0, image.size[0], image.size[1]))

	frame.save(output)
	
def store(images, comic):
	global image_number
	
	dir = os.path.join(output_dir, comic)
	if not os.path.exists(dir):
		os.makedirs(dir)
		
	for image, description in images:
		filename = image.split("/")[-1]
		
		if number_files:
			filename = str(image_number) + "-" + filename
		image_number -= 1
		
		output = os.path.join(dir, filename)
		textfile = os.path.splitext(output)[0] + text_extension
		
		if verbose:
			sys.stderr.write("Downloading '" + image + "' into '" + output + "'\n")
		urllib.urlretrieve(image, output)
		
		if verbose:
			sys.stderr.write("Writing description to '" + textfile + "'\n")
		mktextfile(textfile, description)
		
		if inscribe:
			inscribed = os.path.join(dir, 'i' + filename)
			if verbose:
				sys.stderr.write("Inscribing picture as '" + inscribed + "'\n")
			inscribe(output, description, inscribed);
			
		sys.stderr.write("\n");

if __name__ == '__main__':
	global image_number
	image_number = 0

	name = "xkcd"
	
	images = parse_archive_by_name(name)
	store(images, name)	
	
	
		
