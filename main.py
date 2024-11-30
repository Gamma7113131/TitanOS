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
tcloud = sa.get_tw_cloud("1100152494")
tclient = tcloud.requests(no_packet_loss=True, respond_order="finish")

#Setting up directories
os.makedirs("user_data", exist_ok=True)

@client.event
def on_ready():
    print("[TitanicOS Backend] [scratch] Request handler is running!")

@tclient.event
def on_ready():
    print("[TitanicOS Backend] [turbowarp] Request handler is running!")

@client.request
def ping(username):
    print(f"[TitanicOS Backend] [scratch] Pinged by {username}")
    return "pong"

@tclient.request
def ping(username):
    print(f"[TitanicOS Backend] [turbowarp] Pinged by {username}")
    return "pong"

@client.request
def login(username, password):
    print("[TitanicOS Backend] [scratch] Login request received.")
    response = oslogin.process_login(username, password)
    print(f"[TitanicOS Backend] {response}")
    return response

@tclient.request
def login(username, password):
    print("[TitanicOS Backend] [turbowarp] Login request received.")
    response = oslogin.process_login(username, password)
    print(f"[TitanicOS Backend] {response}")
    return response

@client.request
def check_user(username):
    print(f"[TitanicOS Backend] [scratch] Check user request received for Scratch username: {username}")
    response = oslogin.process_check_user(username)
    print(response)
    return response

@tclient.request
def check_user(username):
    print(f"[TitanicOS Backend] [turbowarp] Check user request received for Scratch username: {username}")
    response = oslogin.process_check_user(username)
    print(response)
    return response

@client.request
def create_account(username, password):
    print(f"[scratch] Create account request received for username: {username}")
    response = oslogin.process_create_account(username, password)
    os.makedirs(f"user_data/{username}")
    print(response)
    return response

@tclient.request
def create_account(username, password):
    print(f"[turbowarp] Create account request received for username: {username}")
    response = oslogin.process_create_account(username, password)
    os.makedirs(f"user_data/{username}")
    print(response)
    return response

@client.request
def bot_ai(model, query, username):
    response = requests.get(f"http://uukelele.ddns.net/duckchat?model={model}&q={query}").content.decode("utf-8")
    with open('capture.log', 'a') as file:
        file.write(f"\n{username} --- Used {model} to request '{query}', and the model responded with '{response}'")
    return response

@tclient.request
def bot_ai(model, query, username):
    response = requests.get(f"http://uukelele.ddns.net/duckchat?model={model}&q={query}").content.decode("utf-8")
    with open('capture.log', 'a') as file:
        file.write(f"\n{username} --- Used {model} to request '{query}'.")
    return response

client.start(thread=True)
tclient.start(thread=True)
