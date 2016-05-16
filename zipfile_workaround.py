#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import zipfile

basedir = u"blabla"
inputfile = sys.argv[1]

zip=zipfile.ZipFile(inputfile)
files = zip.namelist()
print files

for _file in files:
	print "file is", _file
	try:
		print "join is", os.path.join(basedir, _file)
		'''
		The above can give this error with Windows zipped files with special characters in them:

		    print "join is", os.path.join(basedir, _file)
			  File "/usr/lib/python2.7/posixpath.py", line 80, in join
		    path += '/' + b
		'''

	except:
		# the encoding was a problem, so let's assume it was a zip with special CP437 characters in the filename
		print "join is", os.path.join(basedir, _file.decode('cp437'))

