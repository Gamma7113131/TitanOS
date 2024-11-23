import scratchattach as sa
import time
import os
import conversion

session = sa.login("TGammaMCoder","tgmao")
cloud = session.connect_scratch_cloud("1100152494")
client = cloud.requests(no_packet_loss=True,respond_order="finish")

@client.event
def on_ready():
    print("[TitanicOS Backend] Request handler is running!")

@client.request
def ping(username):
    print(f"[TitanicOS Backend] Pinged by {username}")
    return "pong"

client.start(thread=True)