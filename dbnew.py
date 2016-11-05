import boto
import uuid
import boto.s3.connection
from random import Random as _Random
import mysql.connector
import credentials
import csv
import time
import urllib
import os
import pymysql

config = {
'user': credentials.db_username,
'password': credentials.db_password,
'host':credentials.rds_host,
'database': credentials.db_name,
'raise_on_warnings': True
}
cnx = mysql.connector.connect(**config)
cur=cnx.cursor()
s3 = boto.connect_s3(credentials.AWS_ACCESS_KEY_ID, credentials.AWS_SECRET_ACCESS_KEY, is_secure=False)
def upload_to_db():

    print("enter the bucket name:"),
    bucket_name = raw_input()
    bucket = s3.get_bucket(bucket_name)

    all_users = 'http://acs.amazonaws.com/groups/global/AllUsers'

    for key in bucket:
        print str(key).split(",")
        readable = False
        acl = key.get_acl()
        for grant in acl.acl.grants:
            if grant.permission == 'READ':
                if grant.uri == all_users:
                    readable = True
        if not readable:
            key.make_public()

    opens = urllib.URLopener()
    print("enter the filename:"),
    file_name = raw_input()
    link = "wget https://s3.amazonaws.com/" + bucket_name + "/" + file_name
    os.system(link)
    name_list = file_name.split('.')
    filename = name_list[0]
    create_stmt="create table mydatabase.{} (one varchar(20), two varchar(20), three varchar(20))".format(filename)
    cur.execute(create_stmt)
    uploadCSV = """LOAD DATA LOCAL INFILE 'abc.csv' INTO TABLE mydatabase.{} FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES """.format(filename)
    cur.execute(uploadCSV)
    cnx.commit()

upload_to_db()