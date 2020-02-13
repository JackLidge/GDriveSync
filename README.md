## GDriveSync

This program will back up data in a directory to a Google Account with a valid client_secrets.json file in the same directory as it. Can also delete data from the remote Google Drive directory after a certain amount of days if requested. 
Originally based off code in [this repository](https://github.com/SamirStandnes/gdrive_sync_folder_script)

### Usage
```bash
Usage: upload.py [OPTIONS]

  Authenticate access to Google Drive, then proceed to syncing steps if
  successful.

Options:
  -l, --local TEXT   Local folder to be backed up.
  -r, --remote TEXT  Google Drive folder end string.
  --archive INTEGER  Time length of data to be archived.
  --help             Show this message and exit.
```