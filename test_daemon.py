#! /home/lz/anaconda3/bin/python3
# -*- coding: UTF-8 -*-

import time
import daemon

with daemon.DaemonContext():
    while True:
        print('test')
        time.sleep(5)
