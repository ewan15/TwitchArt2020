import shutil
from io import BytesIO
import Twitch
from DBSystem import DBSystem

import websocket
import urllib.request
import ssl
import threading
import os
from dotenv import load_dotenv
import re
from PIL import Image
import requests

from ImageSystem import image_func

load_dotenv()

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect("wss://irc-ws.chat.twitch.tv:443")
ws.send(f"PASS oauth:{os.getenv('OAUTH')}")
ws.send("NICK the_aurelius_")
result = ws.recv()
print("Received '%s'" % result)
ws.send("JOIN #the_aurelius_")
join_conf = ws.recv()
print(f"{join_conf}")
db = DBSystem()

while True:
    recv = ws.recv()
    if 'PING :tmi.twitch.tv' in recv:
        ws.send('PONG :tmi.twitch.tv')
        print("SEDNING PONG")
    else:
        try:
            username,msg = Twitch.break_string(recv)
            msg = msg.rstrip()
            print(f"{username}: {msg}")
            m = re.match(r"(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png|jpeg)",msg)
            if m is not None:
                print("Image found!")
                suffix = msg.split(".")[-1]
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(msg, f"{username}.{suffix}")
                if not Twitch.validate_image(f"{username}.{suffix}"):
                    ws.send("Invalid image: please upload an image of shape 1000px x 1000px")
                else:
                    db.insert_user_image(username,f"{username}.{suffix}")
                    ws.send("PRIVMSG #the_aurelius_ : Image Accepted :) ")
                    img_ls = [i[0] for i in db.fetch_data()]
                    im = image_func(img_ls)
                    im.save("result.png")
                    #im = Image.open(f"{username}.{suffix}")
                    print(f"{recv}")
        except Exception as e:
            print(f"Failed: {recv} with: {e}")
