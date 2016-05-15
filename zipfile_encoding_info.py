#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Use Case:
On Windows, filenames like "Herr Müller.txt" and "privé-something.txt" are represented with Code Page 437 (cp437, which is 8-bit),
and can be zipped into a zip file by the standard Windows tool "... compress ...". So far, so good.

But, if unpacked on Linux (Unicode UTF-8), things go wrong: strange characters instead of the meant ü and é.

The below unzip works on Ubuntu (but not on Debian?):

LANG=en_US.cp437 unzip blablabla.zip
convmv -f cp437 -t utf8 -r * --notest

The tool below will analyse the zip file and *tell* the bare and corrected file name
NB: no file is written. Just an analysis.

Possible output:

Corrected filename: from Deutsch-ist-gef�hlsm��ig-jajaja.txt to Unicode Deutsch-ist-gefühlsmäßig-jajaja.txt
Corrected filename: from Herr-M�ller-ist-zu-hause.txt.txt to Unicode Herr-Müller-ist-zu-hause.txt.txt
Corrected filename: from Michael M�ller - Stad.epub to Unicode Michael Müller - Stad.epub

See https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT, Appendix D about CP437 versus Unicode

'''

import os
import zipfile
import sys

verbose = False
#verbose = True

def ascii(mystring):
    try:
	mystring.decode('ascii')
        return True
    except:
	return False

inFile = sys.argv[1]
if verbose: print "zipfile name is", inFile
fh = open(inFile,'r')
z = zipfile.ZipFile(fh)

for f in z.infolist():
    barefilename = f.filename
    if verbose: print "Bare filename:", barefilename

    '''
    SHORT: The .zip file knows the encoding: it's in bit 11 of the "General purpose bit flag"
    LONG:
    flag_bits is two bytes, with bit 11 meaning:
    - 0: ASCII / CP437
    - 1: Unicode
    See: 
    - https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT, Appendix D (CP 437 versus Unicode)
    - https://en.wikipedia.org/wiki/Zip_(file_format)#File_headers
    '''
   
    if (f.flag_bits & (1<<11) == 0):
	if verbose: print "ZIP-encoding is Plain ASCII / CP437"
	if ascii(barefilename):
		    if verbose: print "filename is ASCII"
		    # ... so nothing needed
	else:
		    if verbose: print "special characters found, so conversion is needed"
		    # not plain ASCII, so special Code Page 437 characters to be decoded, and converted to UTF-8
		    print "Corrected filename: from", barefilename, "to Unicode", barefilename.decode("cp437")           #.encode('utf8')
    else:
	if verbose: print "ZIP-encoding is Unicode, so nothing to do"




