import websocket
import ssl
import threading
import time
import os
from dotenv import load_dotenv
load_dotenv()


# Define a function for the thread
def retrieve_thread(ws):
    recv = ws.recv()
    print(f"{recv}")


def sending_thread(ws):
    ws.send("PRIVMSG #the_aurelius_ :one small step for man one giant leap for memekind")

ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect("wss://irc-ws.chat.twitch.tv:443")
ws.send(f"PASS oauth:{os.getenv('OAUTH')}")
ws.send("NICK the_aurelius_")
result = ws.recv()
print("Received '%s'" % result)
ws.send("JOIN #the_aurelius_")
join_conf = ws.recv()
print(f"{join_conf}")

try:
    ret_thread = threading.Thread(target=retrieve_thread,args=(ws,))
    send_thread = threading.Thread(target=sending_thread,args=(ws,))
    ret_thread.start()
    send_thread.start()
except:
    raise Exception("CANNOT START THREAD")

while True:
    pass
