import os 
from .curlgoogleupload import upload as upload_sdk
from .curlgoogledownload import download as download_sdk
import argparse

def upload():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filepaths", nargs='+', help="Files or directories to include in the zip file")
    parser.add_argument("-r", "--recursive", action="store_true", 
                        help="Zip directories recursively", default=True)
    parser.add_argument("-d", "--directory_id", 
                        help="Google Drive directory ID to upload the zip file to")
    parser.add_argument("-z", "--zip", action="store_true", help="Zip the files",
                        default=True)
    parser.add_argument("-m", "--multifile", action="store_true", help="When set to true every file will be compressed into a zip with name=name and then uploaded")
    parser.add_argument("-n", "--name", help="Name of the zip file")
    args = parser.parse_args()
    
    if args.multifile:
        if args.name is None:
            print("Please specify the name of the zip to aggregate files using -n")
            return
    
    upload_sdk(
        filepaths=args.filepaths,
        zip=args.zip,
        recursive=args.recursive,
        name=args.name,
        directory_id=args.directory_id,
        multifile=args.multifile,
    )

def download():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file_ids", nargs="+", help="Google Drive file ID to download")
    parser.add_argument("-u", "--unzip", action="store_true", 
                        help="Unzip the downloaded file if it's a zip file", default=True)
    args = parser.parse_args()
    
    download_sdk(
        file_ids=args.file_ids,
        unzip=args.unzip,
    )

   