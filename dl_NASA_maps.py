# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 20:37:11 2016

@author: Doug
"""
import requests
import StringIO
import zipfile
import os
import sys
import math
import numpy as np
urly='http://dds.cr.usgs.gov/srtm/version2_1/SRTM3/Eurasia/'
zfn=0
def getfilelist():
    pass
r=requests.get(urly)

file_list=[]
for line in r.iter_lines():
    if line: 
        print line
        href=line.find("a href=")
        zipf=line.find(".zip\"")
        if href>=0 and zipf>=0:
            filename=line[13:zipf+4]
            file_list.append(filename)
            


#extract to dict
def extract_zip(input_zip):
    input_zip=zipfile.ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}

def unzip_draw(filelist):
    #dl file   
    zf=requests.get(urly+filelist,stream=True)    
    zfn=extract_zip(StringIO.StringIO(zf.content))
    print "downloading and extracting "+ filelist+ "..."
    # process into numpy array
    #siz = os.path.getsize(zfn)
    siz = len(zfn[zfn.keys()[0]])
    dim = int(math.sqrt(siz/2))
    print siz
    #assert dim*dim*2 == siz, 'Invalid file size'
    
    data = np.fromstring(zfn[zfn.keys()[0]], np.dtype('>i2'), dim*dim).reshape((dim, dim))
    
    return zfn,map_2_img(cleandatas(data))

maps=[]
for item in file_list[1878:1880]+file_list[1743:1745]:
    maps.append(unzip_draw(item)[1])
gridmap(maps,2,2)

def choosemaptiles():
    map_list=['N37E021','N37E022','N37E023','N36E021','N36E022','N36E023','N35E021','N35E022','N35E023']
