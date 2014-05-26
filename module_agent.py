#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import os
import socket
import json
from datetime import datetime
from apscheduler.scheduler import Scheduler

server_address = '127.0.0.1'
ping_address = '192.168.2.150'
server_port = 8100

ping_status = 0         # 0 - не определено, 1 - компьютер в сети, 2 - компьютер не в сети


def send_activation_message():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_address, server_port))
    data = {'command': 'KEY_ACTIVATE', 'username': 'user', 'password': 'password', 'data': {'KEY_NUMBER': ping_address, 'KEY_DATETIME': datetime.datetime.now()}}
    s.send(bytes(json.dumps(data), 'UTF-8'))


def send_deactivation_message():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_address, server_port))
    data = {'command': 'KEY_DEACTIVATE', 'username': 'user', 'password': 'password', 'data': {'KEY_NUMBER': ping_address, 'KEY_DATETIME': datetime.datetime.now()}}
    s.send(bytes(json.dumps(data), 'UTF-8'))


def job_ping():
    response = os.system("ping -c 1 " + ping_address)
    if response == 0:
        new_ping_status = 1
    else:
        new_ping_status = 2

    if new_ping_status != ping_status:
        response = os.system("ping -c 1 " + ping_address)
        if response == 0:
            new_ping_status = 1
        else:
            new_ping_status = 2

        if new_ping_status != ping_status:
            if new_ping_status == 1:
                send_activation_message()
            else:
                send_deactivation_message()

sched = Scheduler()
sched.start()

sched.add_interval_job(job_ping, minutes=5)
