#!/usr/bin/env python

import socket
import json
import os

import urllib
import urllib2
import httplib2
import time, os, simplejson
import datetime
import csv
OK = 0

#open files for reading and writing
try:
    network = open("network.json", 'w')
    topsites = open("topsites.json" , "rU")
    data = json.load(topsites)
    #TODO modify script so that it can be launched from multiple hosts
    #TODO create a for loop - for row in "rows"
    
    results = data["rows"][0]["doc"]["results"]
    root_name = data["rows"][0]["doc"]["host"]
    name = ', '.join(['{}-{}'.format("ROOT",root_name)])
    
    OK = 1
except IOError:
    print "Could not open file! Please close it..."
    

#define global variables
json_dict = dict({"nodes":[{"group":"root" , "name":name, "radius":12}],"links":[]}) 
name_list = [root_name]
link_dict = {}
# main


if OK == 1:
    nodes = 0
    index1 = 0
    index2 = 0
    value = 1
    duplicate = 0
    group = ""
    
    for k,v in results.items():
        if group != k:
            if group != "":
                name_list.append(group)
                index2 = name_list.index(group)
                json_dict["nodes"].append({"group":group, "name":group, "radius":12, "label": group})
                json_dict["links"].append({"source":index1,"target":index2,"value":value})
            group = k
            index1 = 0
            value = 1
            group_list = [root_name]
        
        routes = {}
        for key, val in v.iteritems():
            routes[int(key)] = val
        routes_dict = routes.iteritems()
              
        for n,i in sorted(routes_dict):
            
            nodes +=1            
            name = ', '.join(['{}-{}'.format(k1,v1) for k1,v1 in i.iteritems()])
            
            if name in name_list:
                if name in group_list:  
                    duplicate +=1
                else:
                    index2 = name_list.index(name)
                    group_list.append(name)
                    json_dict["links"].append({"source":index1,"target":index2,"value":value})
                
            else:
                name_list.append(name)
                group_list.append(name)
                index2 = name_list.index(name)
                json_dict["nodes"].append({"group":group , "name":name, "radius":6,"label": ""})
                json_dict["links"].append({"source":index1,"target":index2,"value":value})
                
            index1 = index2
            value +=1

            
            # delete duplicate links?                
                               

    json.dump(json_dict, network, indent=4, sort_keys=True)
    #network.write(network_dict)
    network.close()
    print "file dumped - see network.json"
    
    print "nodes processed: %d" % nodes
    print "nodes added: %d" % len (json_dict["nodes"])  
    print "links created: %d" % len (json_dict["links"]) 
    print "Length of name_list: %d" % len (name_list)
    print duplicate
    
    print group_list
else:
    print "Something wrong..."
