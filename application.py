import boto
import boto.s3
import sys
import os
from boto.s3.key import Key
from flask import Flask, render_template,request,redirect,url_for,send_from_directory
import time


application= Flask(__name__)
#import logging
#import logging.handlers
#from wsgiref.simple_server import make_server
HOST = str(os.getenv('VCAP_APP_HOST', 'localhost'))
PORT = int(os.getenv('VCAP_APP_PORT', '5050'))

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

bucket_name = AWS_ACCESS_KEY_ID.lower() + '-priyanka3'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
	AWS_SECRET_ACCESS_KEY)

bucket = conn.create_bucket(bucket_name,
    location=boto.s3.connection.Location.DEFAULT)

@application.route("/", methods=['GET'])
def main():
	return render_template('example.html')


def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()	

@application.route('/upload12', methods=['POST'])
def upload():
	

	testfile = request.files['file']
	print"going to upload"
	start=time.time()
	print 'Uploading %s to Amazon S3 bucket %s' % \
		(testfile, bucket_name)

	k = Key(bucket)
	print("print me")
	k.key = testfile.filename
	k.set_contents_from_filename(testfile.filename,
    	cb=percent_cb, num_cb=10)

	end=time.time()
	duration=end-start
	a=round(duration,2)
	print "Time taken: %f" ,a
	
	#html = """
        #<html>
        #<head>
        #<title>Upload file</title>
        #</head>
        #<body>
        #<h1>Success!</h1>
        #<p>Time taken to upload the file to Amazon S3 bucket:%s seconds</p>
        #</body>
        #</html>""" %(round(duration,2))        
        #return html

	return render_template('upload1.html', duration= a)

# Create logger
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)

# Handler 
#LOG_FILE = '/opt/python/log/sample-app.log'
#handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
#handler.setLevel(logging.INFO)

# Formatter
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
#handler.setFormatter(formatter)

# add Handler to Logger
#logger.addHandler(handler)


if __name__ == "__main__":
    application.run(HOST=host, PORT=port)