import uuid
from pathlib import Path
from colorama import Fore
from environs import Env
from pyrogram import Client

env = Env()
env.read_env()

api_id = env.int('API_ID')
api_hash = env.str('API_HASH')
session_path = Path('session')

def add_contacts():
    if session_path.exists():            
        while True:
            with Client(uuid.uuid4().hex, api_id, api_hash) as tmp_app:
                with open(session_path, "a") as file:
                    session_string = tmp_app.export_session_string()
                    if(session_string != None and session_string):
                        file.write(session_string + " ");
            if(input("Write \"stop\" to stop adding a numbers: ") == "stop"):
                break;
        
        print(Fore.GREEN + "The program is configured")
        exit()
    else:
        while True:
            with Client(uuid.uuid4().hex, api_id, api_hash) as tmp_app:
                with open(session_path, 'a') as file:
                    session_string = tmp_app.export_session_string()
                    if(session_string != None and session_string):
                        file.write(session_string + " ")
            if(input("Write \"stop\" to stop adding a numbers: ") == "stop"):
                break;
        
        print(Fore.GREEN +"The program is configured")
        exit()

add_contacts()