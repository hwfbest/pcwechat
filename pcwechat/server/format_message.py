#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/7 16:43
# @Author  : jiaojianglong


class AcceptMassage():

    def __init__(self,msg):
        if msg == "欢迎监听微信消息":  # 连接成功
            self.msg_type = "connect_success"
            return

        msg_list = msg.split("‘")
        if "WXTC" in msg_list:
            self.msg_type = "logout"
            self.botid = msg_list[1]
            return
        from_wxid = msg_list[4]
        text = msg_list[6].strip()
        is_group = False
        member = ""
        if from_wxid.endswith("chatroom"):
            try:
                member = text.split(":")[0]
                a = text.split(":")[1]
                text = text[text.find(":")+1:].strip()
            except:
                text = text
                member = ""
            is_group = True

        self.botid = msg_list[0]
        self.msgid = msg_list[1]
        self.msg_type = msg_list[2]
        self.timenum = msg_list[3]
        self.from_wxid = msg_list[4]
        self.accept_wxid = msg_list[5]
        self.text = text
        self.is_group = is_group
        self.member = member
        if self.is_group:
            self.user_id = self.member
            self.group_id = self.from_wxid
        else:
            self.user_id = self.from_wxid
            self.group_id = ""

    def format(self):
        if self.msg_type == "connect_success":
            return {"type":self.msg_type, "message":self.msg_type}
        elif self.msg_type == "logout":
            return {"type":self.msg_type, "bot_id":self.botid}
        else:
            msg = {
             "bot_id": self.botid,
             "msg_id": self.msgid,
             "date": self.timenum,
             "user_id": self.user_id,
             "group_id": self.group_id,
             "is_group": self.is_group,
             "msg": self.text}
            if self.msg_type == "1":
                msg["type"] = "text"
            elif self.msg_type == "3":
                msg["type"] = "picture"
            elif self.msg_type == "37":  # 加好友申请
                msg["type"] = "addfriend"
            elif self.msg_type == "47":  # 表情
                msg["type"] = "emoticon"
            elif self.msg_type == "43":  # 视屏
                msg["type"] = "vedio"
            elif self.msg_type == "34":  # 语音
                msg["type"] = "voice"
            elif self.msg_type == "42":  #名片
                msg["type"] = "wecard"
            elif self.msg_type == "48":  #位置信息
                msg["type"] = "location"
            elif self.msg_type == "49":  # 连接
                msg["type"] = "link"
            elif self.msg_type == "10000":  # 通知消息
                msg["type"] = "notice"
            elif self.msg_type == "10002":  # 新登录微信
                msg["type"] = "new_bot"
            else:
                print("没有记录的消息类型", self.msg_type)
            return msg
