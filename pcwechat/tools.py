#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-7-6 
# @Author  : JiaoJianglong

import os
import re
import random


def get_port():
    """
    获取可用端口
    :return: 
    """
    # pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
    ports = []
    pscmd = "netstat -ano"
    procs = os.popen(pscmd).read()
    procarr = procs.split("\n")
    for proc in procarr:
        procs = proc.split()
        if procs and procs[0] in ["UDP","TCP"]:
            port = re.search(r".*:(\d+)$",procs[1])
            if port:
                port = port.group(1)
                ports.append(port)
    port1 = random.randint(15000, 20000)
    port2 = random.randint(port1, 20000)
    if port1 not in ports and port2 not in ports:
        return port1, port2
    else:
        get_port()


def transformCode(re_data):
    try:
        re_data = re_data.decode('gbk')
    except Exception as error:

        pos = re.findall(r'position([\d]+):', str(error).replace(' ', ''))
        if len(pos) == 1:
            re_data = re_data[0:int(pos[0])] + re_data[int(pos[0]) + 1:]
            re_data = transformCode(re_data)
            return re_data
    return re_data


def transtoCode(re_data):
    try:
        re_data = re_data.encode('gbk')
    except Exception as error:

        pos = re.findall(r'position([\d]+):', str(error).replace(' ', ''))
        if len(pos) == 1:
            re_data = re_data[0:int(pos[0])] + re_data[int(pos[0]) + 1:]
            re_data = transtoCode(re_data)
            return re_data
    return re_data

if __name__ == '__main__':
    print(get_port())