import dropbox
import datetime

FILE_DESTINATION = '/parko_db/'
DROPBOX_AUTH_KEY = 'token-here'

BACKUP_FILES = [
    {'FILE_NAME': 'test.sql', 'FILE_TYPE': 'sql', 'IDENTIFIER': 'test-backup-file'}

]


def make_backup(file_data):
    # connect to the dropbox applicaton.
    dbx = dropbox.Dropbox(DROPBOX_AUTH_KEY)

    # grab current time and create a path for the file.
    now = datetime.datetime.now()
    path = FILE_DESTINATION + '{}/{}/{}/{}.{}'\
        .format(now.year, now.month, now.day, '{}-{}-{} - {}'
                .format(now.day, now.month, now.year, file_data['IDENTIFIER']), file_data['FILE_TYPE'])

    # open the selected file.
    file = open(file_data['FILE_NAME'], 'rb')

    print("Connected to account " + dbx.users_get_current_account()._name_value.display_name)
    print("Uploading file to dropbox. Destination: " + path)

    # Read the file in and write in to dropbox.
    try:
        bytes = file.read()
        dbx.files_upload(bytes, path)
    finally:
        file.close()

    print("File uploaded. Have a nice day :-)")


for backup_file in BACKUP_FILES:
    make_backup(backup_file)
