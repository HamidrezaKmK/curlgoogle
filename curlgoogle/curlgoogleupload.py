
'''
A Python script to automate curl->googledrive interfacing
This should require nothing more than the system python version and curl. 
Dan Ellis 2020
'''
import os, sys, json, zipfile

if sys.version[0] == '3':
    raw_input = lambda x: input(x)

#Owner information goes here!
from .info import get_client_info

#'1090129644259-6up92q1rak04u9uu13scshf76d5jcqmf.apps.googleusercontent.com'
# client_secret = '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'


def upload(
    filepaths,
    name: str,
    directory_id: str,
    zip: bool = True,
    recursive: bool = True,
):
    """
    This upload function sdk provides a simple interface to upload files to google drive.
    You can enter the directory id and a set of filepaths to upload.
    If zip is set to true, then all the files will be zipped into a single file;
    then, that file would be uploaded into the directory. If recursive is set to true,
    all the files will be recursively iterated.
    
    Args:
        filepaths (list(str)): A list of filepaths to upload.
        zip (bool): Whether to zip the files or not. If set to false, then only 
            the first file in the filepaths list will be uploaded.
        recursive (bool): Whether to recursively iterate through the directories.
        name (str): The name of the zip file.
        directory_id (str): The directory id to upload the file to.
    """
    
    client_id, client_secret = get_client_info()
    
    # get initial auth code
    cmd1 = json.loads(os.popen('curl -d "client_id=%s&scope=https://www.googleapis.com/auth/drive.file" https://oauth2.googleapis.com/device/code'%client_id).read())
    raw_input('\n Enter %(user_code)s\n\n at %(verification_url)s \n\n Then hit Enter to continue.'%cmd1)
    raw_input('(twice)')

    # get token
    cmd2 = json.loads(os.popen(('curl -d client_id=%s -d client_secret=%s -d device_code=%s -d grant_type=urn~~3Aietf~~3Aparams~~3Aoauth~~3Agrant-type~~3Adevice_code https://accounts.google.com/o/oauth2/token'%(client_id,client_secret,cmd1['device_code'])).replace('~~','%')).read())

    # zip files if -z is specified
    remove_file_after_upload = False
    filepath = filepaths[0] # use the first file if not zipping
    if zip:
        with zipfile.ZipFile('%s.zip'%name, 'w') as myzip:
            for path in filepaths:
                if recursive and os.path.isdir(path):
                    for dirpath, dirnames, files in os.walk(path):
                        for name in files:
                            myzip.write(os.path.join(dirpath, name))
                else:
                    myzip.write(path)
        filepath = '%s.zip'%name
        remove_file_after_upload = True

    # upload to drive
    metadata = { "name" : name }
    if directory_id:
        metadata["parents"] = [directory_id]
    metadata_str = json.dumps(metadata) # use json.dumps to properly format the json string
    cmd4 = os.popen('''
    curl -X POST -L -H "Authorization: Bearer %s" -F 'metadata=%s;type=application/json;charset=UTF-8' -F "file=@%s;type=application/zip" "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
    '''%(cmd2["access_token"],metadata_str,filepath)).read()
    
    if remove_file_after_upload:
        os.remove(filepath)
        
    print(cmd4)
    print('end')

