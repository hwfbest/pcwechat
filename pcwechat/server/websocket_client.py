#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-7-6 
# @Author  : JiaoJianglong

import asyncio
import websockets
import json

async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"command":"start_up_client"}))
        # await websocket.send(json.dumps({"command":"start_up_wx","wxclient_id":"88998898"}))
        # await websocket.send(json.dumps({"command":"get_login_code","wxclient_id":"1951019800"}))
        a = await websocket.recv()
        print(a)

async def accept_message(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            a = await websocket.recv()
            print(a)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        accept_message('ws://127.0.0.1:7777')
    )
    # asyncio.get_event_loop().run_until_complete(
    #     hello('ws://127.0.0.1:7777/sss')
    # )
    # asyncio.get_event_loop().run_forever()