#!/usr/bin/python

import socket
import struct
import os
import sys
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
    topsites = open("topsites.csv" , "rU")
    reader = csv.reader(topsites)
    print "Topsites open."
except IOError:
    print "Could not open file! Please close it..."

#routes = open("traceroute.csv", 'w')

#define global variables
site_dict = dict()
trace_dict = dict()


# We want unbuffered stdout so we can provide live feedback for
# each TTL. You could also use the "-u" flag to Python.
#class flushfile(file):
#    def __init__(self, f):
#        self.f = f
#    def write(self, x):
#        self.f.write(x)
#        self.f.flush()

#sys.stdout = flushfile(sys.stdout)

def main(dest_name):
    dest_addr = socket.gethostbyname(dest_name)
    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        
        # Build the GNU timeval struct (seconds, microseconds)
        timeout = struct.pack("ll", 5, 0)
        
        # Set the receive timeout so we behave more like regular traceroute
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
        
        recv_socket.bind(("", port))
        sys.stdout.write(" %d  " % ttl)
        send_socket.sendto("", (dest_name, port))
        curr_addr = None
        curr_name = None
        finished = False
        tries = 3
        while not finished and tries > 0:
            try:
                _, curr_addr = recv_socket.recvfrom(512)
                finished = True
                curr_addr = curr_addr[0]
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
            except socket.error as (errno, errmsg):
                tries = tries - 1
                sys.stdout.write("* ")
        
        send_socket.close()
        recv_socket.close()
        
        if not finished:
            pass
        
        if curr_addr is not None:
            curr_host = "%s (%s)" % (curr_name, curr_addr)
            site_dict[ttl] = {curr_name : curr_addr}
        else:
            curr_host = ""
        sys.stdout.write("%s\n" % (curr_host))

        ttl += 1
        if curr_addr == dest_addr or ttl > max_hops:
            break
# main
print os.getenv("USER")
print os.getenv("SUDO_USER")
hostname = socket.gethostbyname(socket.gethostname())
print hostname
#setup dict for storing traceroutes
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
trace_dict = {'host':hostname, 'datetime': '', 'results': {}}
trace_dict['datetime'] = now

if db_connect == 1:
    
    for i, row in enumerate(reader):
        site = row[0]
        if __name__ == "__main__":
            print site
            main(site)
            #sites_dict[site] = site_dict
            trace_dict['results'][site] = site_dict.copy()
            db.save(trace_dict)
            site_dict.clear()
else:
    print "Couch database not initialized"

