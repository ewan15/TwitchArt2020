import websocket
import urllib.request
import ssl
import threading
import os
from dotenv import load_dotenv
import re
from PIL import Image

load_dotenv()

website_regex = re.compile("(\b(https?|ftp|file)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]",
                           re.IGNORECASE)


# Define a function for the thread
def retrieve_thread(ws):
    while True:
        recv = ws.recv()
        msg = recv.split(':', 2)[-1]
        if re.match(website_regex, msg) is not None:
            print("Found image!")
            urllib.request.urlretrieve(f"{msg}", "test.jpeg")
            im = Image.open(r"test.jpeg")
            im.show()
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
    ret_thread = threading.Thread(target=retrieve_thread, args=(ws,))
    send_thread = threading.Thread(target=sending_thread, args=(ws,))
    ret_thread.start()
    send_thread.start()
except Exception as e:
    raise Exception(f"CANNOT START THREAD:{e}")

while True:
    pass
