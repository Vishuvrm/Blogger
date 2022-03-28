# pip install pydrive
from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tabulate import tabulate
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'F:\FlaskFridays\application\Connect_to_drive\client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 5 files the user has access to.
    """
    service = get_gdrive_service()
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=5, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
    # get the results
    items = results.get('files', [])
    # list all 20 files & folders
    list_files(items)


def list_files(items):
    """given items returned by Google Drive API, prints them in a tabular way"""
    if not items:
        # empty drive
        print('No files found.')
    else:
        rows = []
        for item in items:
            # get the File ID
            id = item["id"]
            # get the name of file
            name = item["name"]
            try:
                # parent directory ID
                parents = item["parents"]
            except:
                # has no parrents
                parents = "N/A"
            try:
                # get the size in nice bytes format (KB, MB, etc.)
                size = get_size_format(int(item["size"]))
            except:
                # not a file, may be a folder
                size = "N/A"
            # get the Google Drive type of file
            mime_type = item["mimeType"]
            # get last modified date time
            modified_time = item["modifiedTime"]
            # append everything to the list
            rows.append((id, name, parents, size, mime_type, modified_time))
        print("Files:")
        # convert to a human readable table
        table = tabulate(rows, headers=["ID", "Name", "Parents", "Size", "Type", "Modified Time"])
        # print the table
        print(table)

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


# service = get_gdrive_service()
# folder1 = "first"
# folder_metadata = {
#             "name": folder,
#             "mimeType": "application/vnd.google-apps.folder"
#         }
# create_folder = service.files().create(body=folder_metadata, fields="id").execute()
# folder_id = {"id": create_folder['id']}
#
# folder2 = "second"
# folder_metadata = {
#             "parents": folder_id,
#             "name": folder,
#             "mimeType": "application/vnd.google-apps.folder"
#         }
# create_folder = service.files().create(body=folder_metadata, fields="id").execute()


## UPLOAD FILES
def upload_files(folder_name, *upload_files):
    """
    Creates a folder and upload a file to it
    """
    # authenticate account
    service = get_gdrive_service()
    # folder details we want to make
    folders = folder_name.split("\\")
    folder_id = None
    for folder in folders:
        # folder_metadata = {
        #     "parents":folder_id,
        #     "name": folder,
        #     "mimeType": "application/vnd.google-apps.folder"
        # }
        # create_folder = service.files().create(body=folder_metadata, fields="id").execute()
        folder_id = createRemoteFolder(folder, folder_id)
        print("Folder ID:", folder_id)

    for upload_file in upload_files:
        file_metadata = {
                        "name": os.path.basename(upload_file),
                        "parents": [folder_id]
                        }
        # full_path = os.path.join(r"../static/uploads/images", upload_file)
        media = MediaFileUpload(upload_file, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id', supportsTeamDrives=True).execute()
        print("File created, id:", file.get("id"))
    # gfile = drive.CreateFile({"parents": [{"id": "1WOUA3RmLv4a5aYe_Z46AgqN4eKqQ1ad2"}]})
    # # read the file and set i t as the content of this instance
    # gfile.SetContentFile(full_path)
    # gfile.Upload()  # Upload the file


## INSERT FILES
def insert_files(folder_id, *upload_files):
    for upload_file in upload_files:
        file_metadata = {
            "name": os.path.basename(upload_file),
            "parents": [folder_id]
        }
        # full_path = os.path.join(r"../static/uploads/images", upload_file)
        media = MediaFileUpload(upload_file, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("File created, id:", file.get("id"))

def delete_specific(fileid):
    service.files().delete(fileId=fileid).execute()

def empty_folder(folder_id):
    # # First, get the folder ID by querying by mimeType and name
    # folderId = service.files().list(q="mimeType = 'application/vnd.google-apps.folder' and name = 'thumbnails'",
    #                               pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # # this gives us a list of all folders with that name
    # folderIdResult = folderId.get('files', [])
    # # however, we know there is only 1 folder with that name, so we just get the id of the 1st item in the list
    # id = folderIdResult[0].get('id')

    # Now, using the folder ID gotten above, we get all the files from
    # that particular folder
    results = service.files().list(q="'" + folder_id + "' in parents", pageSize=10,
                                 fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    for item in items:
        delete_specific(item["id"])

    # Now we can loop through each file in that folder, and do whatever (in this case, download them and open them as images in OpenCV)
    # for f in range(0, len(items)):
    #     fId = items[f].get('id')
    #     fileRequest = drive.files().get_media(fileId=fId)
    #     fh = io.BytesIO()
    #     downloader = MediaIoBaseDownload(fh, fileRequest)
    #     done = False
    #     while done is False:
    #         status, done = downloader.next_chunk()
    # fh.seek(0)
    # fhContents = fh.read()


def createRemoteFolder(folderName, parentID=None):
    # Create a folder on Drive, returns the newely created folders ID
    body = {
        'name': folderName,
        'mimeType': "application/vnd.google-apps.folder"
    }
    if parentID:
        body['parents'] = [parentID]
    root_folder = service.files().create(body=body, supportsTeamDrives=True).execute()
    return root_folder['id']

if __name__ == '__main__':
    main()
    service = get_gdrive_service()
    print("#############################################")
else:
    service = get_gdrive_service()

# empty_folder("1v199JS0cKRDUJE496r9aMrXNdav3l4A-")
# delete_specific("18bj8J9Qty859mmCZemSbynCC00q51eBW")
# insert_files("1f7VeEgV3wn9urf_EzQK-QmRWJYjnKoWB", r"F:\FlaskFridays\application\static\images\home_page_bg.jpg", r"F:\FlaskFridays\application\static\images\search_bright.jpg")
    # createRemoteFolder("second", "1fGz9mkVzDOqGWqivSp3ikxQx1NcaPXG7")
    # folder1 = "first"
    # folder_metadata = {
    #     "name": folder1,
    #     "mimeType": "application/vnd.google-apps.folder"
    # }
    # create_folder = service.files().create(body=folder_metadata, fields="id").execute()
    # folder_id = {"id": create_folder['id']}
    #
    # folder2 = "second"
    # folder_metadata = {
    #     "parents": folder_id,
    #     "name": folder2,
    #     "mimeType": "application/vnd.google-apps.folder"
    # }
    # create_folder = service.files().create(body=folder_metadata, fields="id").execute()
    # upload_files()
    # folder_upload()


