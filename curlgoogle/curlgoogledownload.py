'''
A Python script to automate file download from Google Drive and optional unzipping.
'''
import os, json, requests, zipfile
from .info import get_client_info

def download(
    file_ids: list,
    unzip: bool = True,
):
    """
    This download function sdk provides a simple interface to download files from google drive.
    Using the file_id you can download the file from google drive and if unzip is set to
    true, then the file will be unzipped automatically.

    Args:
        file_id: The file id to download from google drive.
        unzip (bool, optional): Whether to unzip or not. Defaults to True.
    """
    client_id, client_secret = get_client_info()
    
    # get initial auth code
    cmd1 = json.loads(os.popen('curl -d "client_id=%s&scope=https://www.googleapis.com/auth/drive.file" https://oauth2.googleapis.com/device/code'%client_id).read())
    input('\n Enter %(user_code)s\n\n at %(verification_url)s \n\n Then hit Enter to continue.'%cmd1)
    input('(twice)')

    # get token
    cmd2 = json.loads(os.popen(('curl -d client_id=%s -d client_secret=%s -d device_code=%s -d grant_type=urn~~3Aietf~~3Aparams~~3Aoauth~~3Agrant-type~~3Adevice_code https://accounts.google.com/o/oauth2/token'%(client_id,client_secret,cmd1['device_code'])).replace('~~','%')).read())

    for file_id in file_ids:
        # download the file
        filename = 'file_from_drive.zip'
        url = "https://www.googleapis.com/drive/v3/files/%s?alt=media" % file_id
        headers = {"Authorization": "Bearer %s" % cmd2["access_token"]}
        response = requests.get(url, headers=headers)

        # save the file
        with open(filename, 'wb') as f:
            f.write(response.content)

        # unzip the file if -u is specified and the file is a zip file
        if unzip and zipfile.is_zipfile(filename):
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall('.')
            print('File unzipped successfully.')
            # remove the zip file
            os.remove(filename)
        else:
            print('File downloaded successfully.')

