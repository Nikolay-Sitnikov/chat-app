#!/usr/bin/env python3

import _thread
import asyncio

import server
import wsserver

_thread.start_new_thread(server.run, ())
asyncio.get_event_loop().run_until_complete(wsserver.run())
asyncio.get_event_loop().run_forever()
