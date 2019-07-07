#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-7-6 
# @Author  : JiaoJianglong

import subprocess
import threading
import asyncio
from server.format_message import AcceptMassage
import json
import re

from tools import get_port, transformCode, transtoCode
from server_settings import AUTHORIZED_PATH, BASE_DIR


class WXClient():

    def __init__(self, manage_server):
        self.manage_server = manage_server
        self._reconnect_num = 0
        self.EOF = b"\xcd\xea\xb3\xc9"
        #self.send_port, self.accept_port = get_port()
        self.send_port, self.accept_port = 8899, 8898
        self.ioloop = asyncio.get_event_loop()
        self.id = str(self.send_port) + str(self.accept_port)
        print(self.send_port, self.accept_port)

    def start_wxclient(self):
        def run():
            subprocess.call(
                [AUTHORIZED_PATH, "%s|%s|DK494IG0394IYKK549502303IJJJ4949UWDSLMVM949324IBMI52" %
                 (self.accept_port, self.send_port)])
        #threading.Thread(target=run).start()

    async def connect(self):
        self.start_wxclient()
        self.reader, self.writer = await asyncio.wait_for(asyncio.open_connection("localhost", self.accept_port),
                                                      timeout=15)
        message = await self.reader.readuntil(self.EOF)
        message = transformCode(message)
        print(message)
        asyncio.run_coroutine_threadsafe(self.accept_message(), self.ioloop)
        asyncio.run_coroutine_threadsafe(self.hart_beat(), self.ioloop)

        return self

    async def hart_beat(self):
        await asyncio.sleep(30)
        try:
            self.writer.write(self.EOF)
            await self.writer.drain()
            await self.hart_beat()
        except:
            print("心跳异常")

    async def accept_message(self):
        message = await self.reader.readuntil(self.EOF)
        await self.handle_message(message)
        await self.accept_message()

    async def handle_message(self, message):
        message = transformCode(message)
        message = message[:message.find("完成")]
        message = AcceptMassage(message).format()
        await self.manage_server.send_messages.put(message)
        print(message)

    async def send_message(self, message):
        reader, writer = await asyncio.wait_for(asyncio.open_connection("localhost", self.send_port),
                                                          timeout=15)
        writer.write(transtoCode(message))
        await writer.drain()
        await asyncio.sleep(1)
        writer.close()

    async def send_message_return(self, message):
        reader, writer = await asyncio.wait_for(asyncio.open_connection("localhost", self.send_port),
                                                          timeout=15)
        writer.write(transtoCode(message))
        await writer.drain()
        msg = await reader.readuntil(self.EOF)
        writer.close()
        print(msg)
        if msg.startswith(b"CODE"):
            rec_data = msg[:msg.find(b"\xcd\xea\xb3\xc9")]
        else:
            rec_data = transformCode(msg)
            rec_data = rec_data[:rec_data.find("完成")]
        return rec_data

    async def start_up(self):
        await self.send_message("start up")
        return "success"

    async def get_login_code(self):
        msg = await self.send_message_return("QR code")
        return msg

    async def auto_friend(self):
        """
        自动同意加好友
        :return:
        """
        res = await self.send_message_return("Friends")
        status_flag = False
        status = re.search(r"自动通过好友添加验证(?P<status>.*)成功",res).group("status")
        if status == "打开":
            status_flag = True
        return status_flag

    async def auto_group(self):
        """
        自动同意进群
        :return:
        """
        res = await self.send_message_return("group")
        status_flag = False
        status = re.search(r"自动同意进群(?P<status>.*)成功", res).group("status")
        if status == "打开":
            status_flag = True
        return status_flag

    async def get_weixin_bot(self):
        """
        获取微信号
        :return:
        """
        recData = await self.send_message_return("WeChat list")
        if recData.startswith("YXLB"):
            rec = recData.replace("YXLB‘", "")
            if len(rec) > 3:
                weixin_num_list = rec.split("—")
                weixin_list = []
                for weixin_num_str in weixin_num_list:
                    if weixin_num_str:
                        try:
                            weixin_dict = {}
                            weixin_message = weixin_num_str.split("‘")
                            weixin_dict['num'] = weixin_message[0]
                            weixin_dict['nickname'] = weixin_message[1]
                            weixin_dict['phone'] = weixin_message[2]
                            weixin_dict['id'] = weixin_message[3]
                            weixin_dict['wxid'] = weixin_message[4]
                            weixin_list.append(weixin_dict)
                        except:
                            pass
                return weixin_list
        return []

