from google_ import Create_Service

def get_link(id_):
    # return f"https://drive.google.com/thumbnail?id={id_}"
    CLIENT_SECRET_FILE = r'F:\FlaskFridays\application\Connect_to_drive\client_secrets.json'
    API_NAME = 'drive'
    API_VERSION = "v3"
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # Update Sharing Setting
    file_id = id_

    request_body = {
        'role': 'reader',
        'type': 'anyone'
    }

    response_permission = service.permissions().create(
        fileId=file_id,
        body=request_body
    ).execute()


    # Print Sharing URL
    response_share_link = service.files().get(
        fileId=file_id,
        fields='webViewLink'
    ).execute()
    #
    print(response_share_link)

    # Remove Sharing Permission
    # service.permissions().delete(
    #     fileId=file_id,
    #     permissionId='anyoneWithLink'
    # ).execute()

    url = f"https://drive.google.com/uc?export=view&id={id_}"
    return url

if __name__ == "__main__":
    link = get_link('1fivmowygc-f-OVILvxPc22irOgc2jrOa')
    print("==>",link)
