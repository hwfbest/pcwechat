#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/7 19:47
# @Author  : jiaojianglong

from client_settings import SERVER_ADDRS
from client.server_client import ServerClient
import asyncio
class pcwechat():

    def __init__(self,server_addrs=None):
        self._clients = {}
        addrs = server_addrs if server_addrs else SERVER_ADDRS
        for addr in addrs:
            server_client = ServerClient(addr)
            self._clients.update({addr:server_client})
        asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    pcwechat()





