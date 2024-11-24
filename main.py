#Imports
import scratchattach as sa
import oslogin
import os
import requests

#Setup
password = os.getenv('PASSWORD')  # Password stored in environment variable PASSWORD

session = sa.login("uukelele", password)
cloud = session.connect_scratch_cloud("1100152494")
client = cloud.requests(no_packet_loss=True, respond_order="finish")

#Setting up directories
os.makedirs("user_data", exist_ok=True)

@client.event
def on_ready():
    print("[TitanicOS Backend] Request handler is running!")

@client.request
def ping(username):
    print(f"[TitanicOS Backend] Pinged by {username}")
    return "pong"

@client.request
def login(combined_username, password):
    print("Login request received.")
    response = oslogin.process_login(combined_username, password)
    print(response)
    return response

@client.request
def check_user(scratch_username):
    print(f"Check user request received for Scratch username: {scratch_username}")
    response = oslogin.process_check_user(scratch_username)
    print(response)
    return response

@client.request
def create_account(username, password, scratch_username):
    print(f"Create account request received for username: {username}, Scratch username: {scratch_username}")
    response = oslogin.process_create_account(username, password, scratch_username)
    os.makedirs(f"user_data/{scratch_username}")
    print(response)
    return response

@client.request
def bot_ai(model, query, username):
    response = requests.get(f"http://uukelele.ddns.net/duckchat?model={model}&q={query}").content.decode("utf-8")
    with open('capture.log', 'a') as file:
        file.write(f"\n{username} --- Used {model} to request '{query}', and the model responded with '{response}'")
    return response

client.start(thread=True)
