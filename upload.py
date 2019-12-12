import os
import logging
import datetime
from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth

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
        f.write(f"{ftime} | {text}")
    return

def gdrive_sync(gauth, os_root_path, gdrive_root_folder_id):
    '''
    Function which performs the sync operation.
    TODO: Add in function which deletes files from Google Drive which are no longer present in
    local folder.
    '''

    with open('update_log.txt') as f:
        log_info = f.readlines()
        last_line = log_info[-1].strip()
        log_mod_time = last_line.split('|')
        log_mod_time = datetime.datetime.strptime(log_mod_time[0], '%Y-%m-%d %H:%M:%S ')
    
    drive = GoogleDrive(gauth)
    dir_dict = {os_root_path: gdrive_root_folder_id}
    item_list = drive.ListFile({'q': f'"{folder_id}" in parents and trashed=false'}).GetList()
    
    for dirpath, dirnames, files in os.walk(os_root_path):
        for directory in dirnames:
            dir_mod_time = os.path.getmtime(os.path.join(dirpath, directory))
            dir_mod_time = datetime.datetime.fromtimestamp(dir_mod_time)
            
            if dir_mod_time > log_mod_time:
                new_folder = drive.CreateFile({'title': directory, 
                                               'parents':  [{'id': dir_dict[dirpath]}], 
                                               'mimeType': 'application/vnd.google-apps.folder' })
                new_folder.Upload()
                dir_dict[os.path.join(dirpath, directory)] = new_folder['id']
    
        for file in files:
            file_mod_time = os.path.getmtime(os.path.join(dirpath, file))
            file_mod_time = datetime.datetime.fromtimestamp(file_mod_time)
            
            # If the file in the local directory was modified more recently than the last backup
            # was run, upload to Google Drive.
            if file_mod_time > log_mod_time:

                new_file = drive.CreateFile({'title': file, 
                                             'parents': [{'kind': 'drive#fileLink', 
                                                          'id': dir_dict[dirpath]}]})
    
                #Check existing files for the same name file to overwrite if overwritten locally.
                old_file = [item['title'] == file for item in item_list]
                [item.Delete() for i, item in enumerate(item_list) if old_file[i] == True]
                
                #Upload new file.
                new_file.SetContentFile(os.path.join(dirpath, file))
                new_file.Upload()

def upload(path, folder_id):

    """ Initial Authentication, local """
    gauth = GoogleAuth()
    
    gauth.LoadCredentialsFile('credentials.txt')
    if not gauth.credentials:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile('credentials.txt')

	# Empty Gdrive folder
    gdrive_sync(gauth, path, folder_id)
    log2File('update_log.txt', f'Synced with GDrive\n')


""" If you decide to hard code the Google Drive folder ID and Directory Path into the upload function 
	you dont have to read the folder_sync_registrer below. You can just remove the code and uncomment
	the upload call below this section
"""

import csv
with open('folder_sync_registrer.txt', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        folder_id = row[1]
        root_path = row[0]
        upload(row[0], row[1])