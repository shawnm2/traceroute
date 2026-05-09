#!/usr/bin/env python

import socket
import json
import os
import couchdb
import urllib
import urllib2
import httplib2
import time, os, simplejson
import datetime
import csv

# connect to database
couch = couchdb.Server() # by default localhost:5984
#couch = couchdb.Server('http://prl.iriscouch.com:5984/')
# or use commandline curl -X GET http://prl.iriscouch.com:5984/traceroute/_all_docs?include_docs=true > topsites.json

db_connect = 0
try:
    db = couch['traceroute']
    print "db connection successful"
    print db
    db_connect = 1
except: # catch *all* exceptions
    pass


#open files for reading and writing
try:
    sites = open("topsites.json", 'w')
except IOError:
    print "Could not open file! Please close it..."

#define global variables
sites_dict = dict() 
            
# main
print os.getenv("USER")
print os.getenv("SUDO_USER")
hostname = socket.gethostbyname(socket.gethostname())
print hostname

if db_connect == 1:
    response = urllib2.urlopen('http://localhost:5984/traceroute/_all_docs?include_docs=true')
    #response = urllib2.urlopen('http://prl.iriscouch.com:5984/traceroute/_all_docs?include_docs=true')

    #html = response.read()
    content = response.read()
    sites.write(content)
    sites.close()
    print "file dumped - see topsites.json"                
        
else:
    print "Couch database not initialized"
