"""
This file only contains a piece of code to get the client information
"""
import os
from dotenv import load_dotenv

def get_client_info():
    load_dotenv()
    # returns client_id and client_secret
    try:
        client_id = os.environ['GDRIVE_CLIENT_ID']
        client_secret = os.environ['GDRIVE_CLIENT_SECRET']
    except Exception as e:
        raise Exception("You must call curlgoogle.setup() before using any of the functions.")
    
    return client_id, client_secret
