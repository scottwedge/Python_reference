#!/usr/bin/python

import os
import sys
import time
import requests
import json
import mypaths
from readYamlConfig import readYAMLConfigs
from L1commonFunctions import *
##########################################################################
#   GET household
##########################################################################
def doit(cfg,printflg=False):
    # announce
    disable_warning()   #Method Called to suppress all warnings
    abspath = os.path.abspath(__file__)
    scriptName = os.path.basename(__file__)
    (test, ext) = os.path.splitext(scriptName)
    print "Starting test " + test
    name = (__file__.split('/'))[-1]
    I = 'Core DVR Functionality'     #rally initiatives  
    US = 'GET household'
    TIMS_testlog = []
    TIMS_testlog = [name,I,US]

    # set values based on config
    protocol = cfg['protocol']
    hosts = get_hosts_by_config_type(cfg,'upm',printflg)
    if hosts == None :
        msg = 'testcase failed :Host not found'
        print msg
        TIMS_testlog.append(1)
        TIMS_testlog.append(msg)
        return TIMS_testlog
    port = cfg['upm']['port']
    prefix = cfg['sanity']['household_prefix']
    throttle_milliseconds = cfg['sanity']['throttle_milliseconds']
    if throttle_milliseconds < 1:
        throttle_milliseconds = 25
    headers = {
      'Accept': 'application/json',
      'Source-Type': 'WEB',
      'Source-ID': '127.0.0.1',
    }
    timeout = 2
    any_host_pass = 0
    for index, host in enumerate(hosts):
        if index > 1:
            time.sleep(throttle_milliseconds / 1000.0 )
        householdid = prefix + str(index)
        url = protocol + "://" + host + ":" + str(port) + "/upm/households/" + householdid
        r = sendURL ("get",url,timeout,headers)
        print "Get Household via ", url        
        if r is not None :
            if ( r.status_code != 200):
                print "Problem accessing: " + url
                print r.status_code
                print r.headers
                print r.content
            else:
                if r.content is None :
                    print "\n" + "#"*20 + " DEBUG STARTED "+ "#"*20+ "\n"
                    print "Get Household result \n"+json.dumps(json.loads(r.content),indent = 4, sort_keys=False)
                    print "\n" + "#"*20 + " DEBUG ENDED   "+ "#"*20+ "\n"
                any_host_pass = any_host_pass + 1
                printLog("Get Household result \n"+json.dumps(json.loads(r.content),indent = 4, sort_keys=False),printflg)
    if any_host_pass :
         msg = 'Testcase passed :Get Household ran successfully.'
         print msg
         TIMS_testlog.append(0)
         TIMS_testlog.append(msg)
         return TIMS_testlog

    else:
         msg = 'Testcase failed :Get Household was not successful.'
         print msg
         TIMS_testlog.append(1)
         TIMS_testlog.append(msg)
         return TIMS_testlog

if __name__ == '__main__':
    scriptName = os.path.basename(__file__)
    #read config file 
    sa = sys.argv
    cfg = relative_config_file(sa,scriptName)
    if cfg['sanity']['print_cfg']:
         print "\nThe following configuration is being used:\n"
         pprint(cfg)
         print
    L = doit(cfg, True)
    exit(L[3] )

