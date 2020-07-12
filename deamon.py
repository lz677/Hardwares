#! C:\Users\93715\Anaconda3\python.exe
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
import test

with daemon.DaemonContext():
    while True:
        test.test()
