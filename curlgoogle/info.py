"""
This file only contains a piece of code to get the client information
"""
import os
from dotenv import load_dotenv
from getpass import getpass

def get_client_info():
    # retrieve client id and client secret
    load_dotenv()
    # returns client_id and client_secret
    
    try:
        client_id = os.environ['GDRIVE_CLIENT_ID']
        client_secret = os.environ['GDRIVE_CLIENT_SECRET']
    except Exception as e:
        print("client id and secret not found in environment ...")
        print("-----------------------------------")
        print("[IMPORTANT] to avoid entering every time, try adding them as environemnt variables:")
        print("\tpip install python-dotenv")
        print("\tdotenv set GDRIVE_CLIENT_ID <your_client_id>")
        print("\tdotenv set GDRIVE_CLIENT_SECRET <your_client_secret>")
        print("-----------------------------------", end='\n\n')
        print("Entering manual mode ...")
        client_id = input('Enter client id: ')
        client_secret = getpass(prompt='Enter client secret: ')
        
    return client_id, client_secret
