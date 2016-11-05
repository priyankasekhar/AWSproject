import boto
import uuid
#import boto.s3.connection
#import mysql.connector
import csv
import time
import urllib
import pymysql
import random
import sys
from itertools import *
import credentials
import boto.ec2
import memcache


def memcache_query():
    result={}
    global count
    #memcache.flush_all()
    mc = memcache.Client(['cluster2.uxoww4.cfg.usw2.cache.amazonaws.com:11211'])
    print mc
    print "enter the table name:",
    filename = raw_input()
    cur = cnx.cursor()
    count_query='SELECT COUNT(*) FROM {}'.format(filename)
    cur.execute(count_query)
    count_res=cur.fetchall()
    for row in count_res:
        count=row[0]
    before_time = time.time()
    print("enter the number of times")
    times=int(raw_input())
    for i in range(0,times):
        rand_number = random.randrange(0, count)
        query = 'SELECT * FROM {} where table_id={}'.format(filename,rand_number)
        print rand_number
        key = str(rand_number)
        if mc.get(key) is not None:
            result[str(key)]= mc.get(key)
            print ("from memcache")
        else:
            cur.execute(query)
            res= cur.fetchall()
            print res
            for row in res:
                key=row[0]
            print(key)
            print("from rds")
            mc.add(str(key),res)
            result[str(key)]=res
    print result
    after_time = time.time()
    total_time=after_time-before_time

    print "Time taken to execute select query with memcache 10 " + " times = " + str(total_time) + " seconds"
    return total_time

def random_gen():
    print("enter the number of times")
    times = int(raw_input())
    beforeTime = time.time()
    print "enter the table name:",
    filename = raw_input()
    with cnx.cursor() as cur :
        for i in range(1, times):
            rand_number = random.randrange(0, count)
            query = 'SELECT * FROM {} where table_id={}'.format(filename, rand_number)
            cur.execute(query)
            print(cur.fetchall())
    afterTime = time.time()
    timeDifference = afterTime - beforeTime
    print "Time difference: "
    print timeDifference
    return timeDifference


cnx = pymysql.connect(credentials.rds_host, user=credentials.db_username, passwd=credentials.db_password,
                      db=credentials.db_name)
ran_time=random_gen()
mem_time=memcache_query()
time_diff=ran_time-mem_time
