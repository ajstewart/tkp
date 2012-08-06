#!/usr/bin/python

import sys, os, time
from itertools import count
import logging
import tkp.database.siputils as sip

import monetdb.sql as db
from monetdb.sql import Error as Error

#host = sys.argv[1] # db host name

db_type = "MonetDB"
db_host = "togano"
db_port = 60200
db_dbase = "sipfull"
db_user = "sipfull"
db_passwd = "sipfull"

conn = db.connect(hostname=db_host,port=db_port,database=db_dbase,username=db_user,password=db_passwd)

starttime = time.time()
basedir = os.getenv("HOME") + '/log/tkp'

print "\nResults will be stored in", db_type, "dbname:", db_dbase

logtime = time.strftime("%Y%m%d-%H%M")
logfile = basedir + '/cross_assoc_cats_' + db_type + '_' + db_dbase + '_' + logtime + '.log'
log = open(logfile, 'w')
#log.write('-')

query = 0
#query_time = []
sql_st = []

try:
    t_start = time.time()
    cursor = conn.cursor()

    """
    This corresponds to missing less than 0.1% of the assocs
    """
    #deRuiter_r = 6./3600.
    
    #ra_min = 284.
    #ra_max = 292.
    #decl_min = 1.
    #decl_max = 9.
    ra_min = 0.
    ra_max = 360.
    zone_min = -41
    zone_max = 90
    #c = [4, 5, 6, 3] # You have to know the ids ;) VLSS, WENSS main, WENSS polar, NVSS, resp.
    c = [4, 5, 6, 3] 
    #sip.load_lite_catalogedsources(conn, c, ra_min, ra_max, decl_min, decl_max)
    sip.cross_associate_cataloged_sources(conn, c, zone_min, zone_max)
    #dbu.variability_detection(conn, dataset.id, 0.2, 3.0)
    t_proc = time.time() - t_start
    print "processing: t =", str(t_proc), "s"
    #sip.get_merged_catalogs(conn, 288., 5., 3600.)
    log.write(str(t_proc) + "\n") 

    conn.close()
    log.close()
except db.Error, e:
    logging.warn("Failed on query nr %s reason: %s " % (query, e))
    log.write("Failed on query nr %s reason: %s " % (query, e))
    log.close()
    logging.debug("Failed query nr: %s, reason: %s" % (query, e))
