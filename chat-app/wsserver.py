#!/usr/bin/env python3

import asyncio
import json
import logging
import websockets
import time # for timestamped messages

logging.basicConfig()

from config import INNER_IP as INNER_IP_ADDRESS

MESSAGES_SINCE_BACKUP = 0
MESSAGES = []

USERS = set()

def generate_message_json():
    if len(MESSAGES) >= 2:
        old_ts = MESSAGES[-2]["timestamp"]
    else:
        old_ts = 0
    new_ts = MESSAGES[-1]["timestamp"]
    message = MESSAGES[-1]["message"]
    return json.dumps({"type":"update","old_timestamp":old_ts,"new_timestamp":new_ts,"message":message})

async def notify_all(message):
    if USERS:
        print(">",message)
        await asyncio.wait([user.send(message) for user in USERS])

async def send_message(message):
    MESSAGES.append({"timestamp": int(time.time()), "message": message})
    await notify_all(generate_message_json())

async def save_to_file(file):
    with open(file, "x") as fp:
        for message in MESSAGES:
            fp.write(message["message"] + "\n")

async def handle_autosave():
    ts = time.gmtime(time.time())
    file = "./backups/%i%i%i-%i.%i-backup.txt" % ts[:5]
    await save_to_file(file)
    await send_message("[SERVER %s] Auto-saved messages to %s" % (time.asctime(ts), file))

async def register(websocket):    
    USERS.add(websocket)

async def unregister(websocket):
    USERS.remove(websocket)
    websocket.close()

async def main_connect(websocket, path):
    global MESSAGES_SINCE_BACKUP
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    print("USER JOIN")
    try:
        # First Update, get ALL info
        await websocket.send('{"type":"data","data":%s}' % (json.dumps(MESSAGES),))
        # Recieving Loop
        async for message in websocket:
            print("<", message)
            data = json.loads(message)
            if data['action'] == 'send': # Send Message
                await send_message(data["text"])
                MESSAGES_SINCE_BACKUP += 1
                if MESSAGES_SINCE_BACKUP % 10 == 0:
                    await handle_autosave()
            elif data["action"] == "replicate":
                await websocket.send(
                    '{"type":"replicate","data":%s}' % (
                        json.dumps(list(filter(lambda x: x["timestamp"] > data["timestamp"], MESSAGES))),
                        )
                    )
            elif data["action"] == "clear":
                if data["password"] == "stopspam" and isinstance(data["index"], int):
                    del MESSAGES[data["index"]]
                    await notify_all('{"type":"data","data":%s}' % (json.dumps(MESSAGES),))
            else:
                logging.error(
                    "unsupported event: {}", data)
    finally:
        print("USER LEAVE")
        await unregister(websocket)
    return

def run():
    return websockets.serve(main_connect, INNER_IP_ADDRESS, 5678)
