import dropbox
import datetime
import schedule
import time

FILE_DESTINATION = '/sql_backups/'
DROPBOX_AUTH_KEY = 'token-here'

# if this is set to true, the format for uploading files will be year/month/day
# otherwise every file will be under FILE_DESTINATION path.
ORGANIZE_FOLDERS_AFTER_DATE = True

# local files that should be sent to dropbox.
BACKUP_FILES = [
    {'FILE_NAME': 'example-file1.sql', 'FILE_TYPE': 'sql', 'IDENTIFIER': 'example-file1'},
    {'FILE_NAME': 'example-file2.sql', 'FILE_TYPE': 'sql', 'IDENTIFIER': 'example-file2'}

]


# this will create a backup of a file dict
def make_backup(file_data, dbx):

    # grab current time and create a path for the file.
    now = datetime.datetime.now()

    # for sorting by date by directories. Current format is; year/month/day
    if ORGANIZE_FOLDERS_AFTER_DATE:
        path = FILE_DESTINATION + '{}/{}/{}/{}.{}'\
            .format(now.year, now.month, now.day, '{}-{}-{} - {}'
                    .format(now.day, now.month, now.year, file_data['IDENTIFIER']), file_data['FILE_TYPE'])

    # for sorting into the same directory.
    else:
        path = FILE_DESTINATION + '{}-{}-{} - {}'\
            .format(now.day, now.month, now.year, file_data['IDENTIFIER'], file_data['FILE_TYPE'])

    # open the selected file.
    file = open(file_data['FILE_NAME'], 'rb')

    print("Uploading file '{}' to dropbox. Destination: {}".format(file_data['FILE_NAME'], path))

    # Read the file in and write in to dropbox.
    try:
        bytes = file.read()
        dbx.files_upload(bytes, path)
    finally:
        file.close()



def job():
    # connect to the dropbox applicaton.
    dbx = dropbox.Dropbox(DROPBOX_AUTH_KEY)

    print("Connected to account " + dbx.users_get_current_account()._name_value.display_name)

    # for every file inside BACKUP FILES, send them to backup method.
    for backup_file in BACKUP_FILES:
        make_backup(backup_file, dbx)

    print("job uploaded. Have a nice day :-)")

# schedule the job for every day at 00:10 o clock.
schedule.every().day.at("00:10").do(job)

# now run a check every minute to check if there is any pending schedules.
while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

