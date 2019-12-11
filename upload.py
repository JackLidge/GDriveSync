import logging
from pydrive.drive import GoogleDrive 
from delete_items_in_gdrive_folder import delete_items_in_gdrive_folder
from upload_handler import upload_handler
from pydrive.auth import GoogleAuth
from datetime import datetime

def log_init(logfilename, logname):
    '''
    Initialising logging configuration
    '''
    log = logging.getLogger(logname)
    log.setLevel(logging.DEBUG)

    log_handler = logging.handlers.RotatingFileHandler(filename=logfilename,
                                                       maxBytes=102400, backupCount=5)
    log_handler.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter(fmt='%(asctime)s | %(name)-18s | %(levelname)-8s | %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
    log_handler.setFormatter(log_formatter)
    log.addHandler(log_handler)
    return log

def log2File(filename, text):
    '''
    log2File makes the process of writing out information to individual files clearer
    and easier to perform.
    '''

    with open(filename, 'a') as f:
        time = datetime.datetime.now()
        ftime = datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
        f.write(f"{ftime}: {text}")
    return

def upload(path, folder_id):

	""" Initial Authentication, local """
	gauth = GoogleAuth()
	gauth.LocalWebserverAuth()

	# Gdrive folder id, if you want hard code it
	#folder_id = ''
	
	#print(drive, vars(gauth))

	# Empty Gdrive folder
	delete_items_in_gdrive_folder(gauth, folder_id)

	#Path to folder for sync if you want to hard code it
	#path = '' 

	#Upload handler for folder path and Grdrive folder
	upload_handler(gauth, path, folder_id)
    log2File('update_log.txt', f'Synced with GDrive\n')


""" If you decide to hard code the Google Drive folder ID and Directory Path into the upload function 
	you dont have to read the folder_sync_registrer below. You can just remove the code and uncomment
	the upload call below this section
"""

import csv
with open('folder_sync_registrer.txt', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
    	upload(row[0], row[1])
    	


#upload()	



	

