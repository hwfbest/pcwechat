#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/7 20:01
# @Author  : jiaojianglong

import asyncio
import websockets
import json


class ServerClient():

    def __init__(self, addr):
        self.accept_addr = addr
        self.send_addr = addr+"/send"
        self.ioloop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self.accept_message(self.accept_addr),self.ioloop)

    async def accept_message(self, uri):
        async with websockets.connect(uri) as websocket:
            while True:
                data = await websocket.recv()
                data = json.loads(data)
                print(data)

    async def send_message(self, message):
        async with websockets.connect(self.send_addr) as websocket:
            await websocket.send(json.dumps(message))

    async def send_message_return(self, message):
        async with websockets.connect(self.send_addr) as websocket:
            await websocket.send(json.dumps(message))
            data = await websocket.recv()
            data = json.loads(data)
            return data