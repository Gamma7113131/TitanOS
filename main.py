import scratchattach as sa
import time
import os
import conversion
import requests

session = sa.login("username", os.getenv("PASSWORD"))
cloud = session.connect_scratch_cloud("1100152494")
client = cloud.requests(no_packet_loss=True,respond_order="finish")

@client.event
def on_ready():
    print("[TitanicOS Backend] Request handler is running!")

@client.request
def ping(username):
    print(f"[TitanicOS Backend] Pinged by {username}")
    return "pong"

@client.request
def bot_ai(model, query, username):
    response = requests.get(f"http://uukelele.ddns.net/duckchat?model={model}&q={query}").content.decode("utf-8")
    with open('capture.log','a') as file:
        file.write("\n{username} --- Used {model} to request '{query}', and the model responded with '{response}'")
    return response

client.start(thread=True)
