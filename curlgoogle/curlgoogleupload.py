
'''
A Python script to automate curl->googledrive interfacing
This should require nothing more than the system python version and curl. 
Dan Ellis 2020
'''
import os, sys, json, zipfile
import typing as th

if sys.version[0] == '3':
    raw_input = lambda x: input(x)

from .info import get_client_info


def upload(
    filepaths,
    directory_id: str,
    name: th.Optional[str] = None,
    zip: bool = True,
    recursive: bool = True,
    multifile: bool = False,
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
    if not multifile:
        for i, filepath in enumerate(filepaths):
            # get the name of filepath if it is not a directory
            
            print(f"uploading file [{i+1}/{len(filepaths)}]")
            with zipfile.ZipFile('%s.zip'%filepath, 'w') as myzip:
                if recursive and os.path.isdir(filepath):
                    for dirpath, dirnames, files in os.walk(filepath):
                        for name_ in files:
                            myzip.write(os.path.join(dirpath, name_))
                else:
                    myzip.write(filepath)
            file_path = '%s.zip'%filepath
            remove_file_after_upload = True
            # upload to drive
            metadata = { "name" : filepath }
            if directory_id:
                metadata["parents"] = [directory_id]
            metadata_str = json.dumps(metadata) # use json.dumps to properly format the json string
            cmd4 = os.popen('''
            curl -X POST -L -H "Authorization: Bearer %s" -F 'metadata=%s;type=application/json;charset=UTF-8' -F "file=@%s;type=application/zip" "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
            '''%(cmd2["access_token"],metadata_str,file_path)).read()
            
            if remove_file_after_upload:
                os.remove(file_path)
                
            print(cmd4)
            print('end')
            print("=====", end='\n\n')
    else:
        filepath = filepaths[0] # use the first file if not zipping
        if zip:
            with zipfile.ZipFile('%s.zip'%name, 'w') as myzip:
                for path in filepaths:
                    if recursive and os.path.isdir(path):
                        for dirpath, dirnames, files in os.walk(path):
                            for name_ in files:
                                myzip.write(os.path.join(dirpath, name_))
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

