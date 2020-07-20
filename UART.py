#! C:\Users\93715\Anaconda3\python.exe
# *-* coding:utf8 *-*
"""
@author: LiuZhe
@license: (C) Copyright SJTU ME
@contact: LiuZhe_54677@sjtu.edu.cn
@file: UART.py
@time: 2020/7/13 16:23
@desc: LESS IS MORE
"""
import serial
import time

# def send(text: str = "helloWorld"):
#     try:
#         while True:
#             ser.write(text.encode("utf-8"))  # 发送一个字符串
#             time.sleep(3)
#     except KeyboardInterrupt:
#         print("程序被外部中断")
#
#
# def receive():
#     try:
#         while True:
#             count = ser.in_waiting()  # 得到当前未接收的数据有多少个
#             if count:
#                 recv = ser.read(count)  # 将这么多数据全部读取出来
#                 print(recv)
#                 ser.flushInput()  # 清空缓冲区域
#             time.sleep(0.1)  # 检测时间间隔
#     except KeyboardInterrupt:
#         print("程序被外部中断")
#
#
# def receive_and_send():
#     while True:
#         # 获得接收缓冲区字符
#         count = ser.inWaiting()
#         if count != 0:
#             # 读取内容并显示
#             recv = ser.read(count)
#             # ser.write(recv)  # 将接受的数据发送出去
#             print(recv)  # 将接受的数据输出
#             # 清空接收缓冲区
#         ser.flushInput()
#         # 必要的软件延时
#         time.sleep(0.1)


def receive_and_send_once():
    # 打开串口
    ser = serial.Serial('/dev/ttyAMA0', 115200)
    if not ser.isOpen:
        ser.open()  # 打开串口
    # 获得接收缓冲区字符
    ser.write(b"D")
    time.sleep(0.1)
    count = ser.inWaiting()
    if count:
        # 读取内容并显示
        recv = ser.read(count)
        ser.flushInput()
        ser.close()
        # ser.write(recv)  # 将接受的数据发送出去
        print(recv)  # 将接受的数据输出
        # 清空接收缓冲区


if __name__ == '__main__':
    try:
        # # 打开串口
        # ser = serial.Serial('/dev/ttyAMA0', 115200)
        # if not ser.isOpen:
        #     ser.open()  # 打开串口
        # # ser.write(b"hi 677 Raspberry pi is ready ")
        # ser.write(b"D")
        # time.sleep(0.1)
        receive_and_send_once()
        # if ser is not None:
        # ser.close()
    except KeyboardInterrupt:
        print('中断')
        # if ser is not None:
        # ser.close()
