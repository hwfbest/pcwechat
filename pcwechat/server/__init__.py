#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-7-6 
# @Author  : JiaoJianglong

import asyncio
import websockets
import json

from server.wxclient import WXClient


class ManageServer():

    def __init__(self, port):
        self._wxclient = {}
        self.send_messages = asyncio.Queue()
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self.echo, 'localhost', port))
        asyncio.get_event_loop().run_forever()

    async def echo(self, websocket, path):
        if path == "/":
            self.send_websocket = websocket  #消息传播只支持一个连接
            while True:
                msg = await self.send_messages.get()
                await self.send_websocket.send(json.dumps(msg))
        else:
            try:
                async for message in websocket:
                    await self.handle_message(message, websocket)
            except websockets.exceptions.ConnectionClosed as e:
                print("连接断开")

    async def handle_message(self, message, websocket):
        data = json.loads(message)
        command = data.get("command")
        if command == "start_up_client":  #启动wxclient
            wxclient = await WXClient(self).connect()
            self._wxclient.update({wxclient.id: wxclient})
            print(wxclient.id)
            await websocket.send(json.dumps({"wxclient_id":wxclient.id}))

        elif command == "start_up_wx":  #启动微信
            wxclient_id = data.get("wxclient_id")
            message = await self.wxclient(wxclient_id).start_up()
            await  websocket.send(json.dumps({"message":message}))

        elif command == "get_login_code":
            code = await self.wxclient(data.get("wxclient_id")).get_login_code()
            await websocket.send(json.dumps({"code":code}))

        elif command == "get_weixin_bot":
            bots_result = await self.wxclient(data.get("wxclient_id")).get_weixin_bot()
            if data.get("bot_id"):
                bot = [bot for bot in bots_result if bot["num"] == data.get("bot_id")]
                bots_result = bot[0] if bot else {}
            await websocket.send(json.dumps({"bot":bots_result}))

        elif command == "auto_friend":
            await self.wxclient(data.get("wxclient_id")).auto_friend()
        else:
            await websocket.send("听不懂你在说什么")

    def wxclient(self, wxclient_id):
        wxclient = self._wxclient.get(wxclient_id)
        if not wxclient:
            raise Exception("wxclient_id错误")
        return wxclient
        


if __name__ == '__main__':
    ManageServer(7777)
