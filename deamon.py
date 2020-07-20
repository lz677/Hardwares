#! /home/lz/anaconda3/bin/python3
# *-* coding:utf8 *-*
"""
@author: LiuZhe
@license: (C) Copyright SJTU ME
@contact: LiuZhe_54677@sjtu.edu.cn
@file: deamon.py
@time: 2020/7/10 20:54
@desc: LESS IS MORE
"""

import daemon
import time


def test():
    with open('/home/lz/Documents/PythonProjects/Hardwares/log.txt', "a+") as f:
        f.write('test\n')


with daemon.DaemonContext():
    while True:
        test()
        time.sleep(5)
