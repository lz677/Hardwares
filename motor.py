#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 6/6/20 10:41 AM
# @Author   : LIU ZHE
# @Site     :
# @File     : motor.py
# @Software : PyCharm
# @License  : (C) Copyright LIU ZHE SJTU.
# @Desc     : 步进电机控制 42步进电机  驱动器：42步进电机驱动器模块一体化驱动微小型步进驱动ZD-M42P
"""
电机：
        相数：2
        不距角：1.8+-0.09
        额定电压：3.8v-12v
        额定电流：DC 1.5A/相  用于调节电位器使驱动器的Ref与GND之间的电压为0.75V
驱动器：
        步进角细分
        M0      M1      M2      细分
        ON      ON      ON      1
        OFF     ON      ON      2
        ON      OFF     ON      4
        OFF     OFF     ON      8
        ON      ON      OFF     16
        OFF     ON      OFF     32

        Indexer接口
        COM 共阳极（3.3-5V）或共阴极（12-24V）
        DIR 方向
            0V or Vcom
        STP PWM 100-20KHz
            0V or VCom
        EN 使能
            0V or VCom

        转速(r/s) 与 脉冲频率（Hz）的关系
        V=P*θe/360/m
        V：电机转速(r/s) P：脉冲频率(Hz) θe：电机固有步距角 m：细分数(整步为 1，半步为 2)
"""

import numpy as np
import os
import datetime

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("导入RPi.GPIO失败")
import time

# time.sleep(5)
GPIO.setmode(GPIO.BOARD)  # 编号方式采用BOARD

# pin_COM = 31  # COM 3.3-5v 采用共阳极
# pin_DIR = 33  # DIR direction 方向信号 0V Vcom
# pin_STP = 35  # STP 步进信号 100-20KHz
# pin_EN = 37  # 脱机信号 Vcom使能电机 0V步进电机脱机状态
# pins = (31, 33, 35, 37)
pin_COM = 32  # COM 3.3-5v 采用共阳极
pin_DIR = 36  # DIR direction 方向信号 0V Vcom
pin_STP = 38  # STP 步进信号 100-20KHz
pin_EN = 40  # 脱机信号 Vcom使能电机 0V步进电机脱机状态
pins = (32, 36, 38, 40)

pin_NC = 13  # NC: pin13
pin_NO = 15  # NO: pin15
pins_travel_switch = (13, 15)

# 初始化
for pin in pins_travel_switch:
    GPIO.setup(pin, GPIO.IN)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)  # 将引脚均设置为输出模式

# 打开状态
switch_1_open = GPIO.input(pin_NC)
# 关闭状态
switch_1_close = GPIO.input(pin_NO)


def init():
    GPIO.output(pin_COM, True)
    GPIO.output(pin_DIR, True)
    GPIO.output(pin_STP, False)
    GPIO.output(pin_EN, False)


def enable_or_disable(is_enable: bool):
    GPIO.output(pin_EN, is_enable)


def cw_or_ccw(is_cw: bool):
    GPIO.output(pin_DIR, is_cw)


def clearup():
    GPIO.cleanup()  # 清除引脚的引用


# def motor_on(frequency: int, subdivide: int):
#     if subdivide in (1, 2, 4, 8, 16, 32) and frequency:
#         pwm = GPIO.PWM(pin_STP, 50)  # 初始化PWM实例 频率为50Hz
#         pwm.start(0)  # 开始脉宽调制，参数范围为0->100


def main():
    print("程序开始")
    init()
    enable_or_disable(True)
    cw_or_ccw(False)
    pwm = GPIO.PWM(pin_STP, 400)  # 初始化PWM实例 频率为100-20kHz 1600 -> 1r/s
    pwm.start(0)  # 开始脉宽调制，参数范围为0->100
    print("进入循环")
    try:
        while True:
            # 行程开关没闭合
            if GPIO.input(pin_NC) == 1 or GPIO.input(pin_NO) == 0:
                pwm.ChangeDutyCycle(0)  # 修改占空比
            # 行程开关闭合
            elif GPIO.input(pin_NO) == 1 and GPIO.input(pin_NC) == 0:
                pwm.ChangeDutyCycle(50)
            # 打开状态
            # switch_1_open = GPIO.input(pin_NC)
            # 关闭状态
            # switch_1_close = GPIO.input(pin_NO)
            # n += 1
            # time.sleep(0.1)  # 0.1 有效果    1.8-2.5V
    except KeyboardInterrupt:
        print("程序结束")
        pwm.stop()  # 停止输出PWM波
        clearup()  # 清空GPIO
        # enable_or_disable(False) # 不释放GPIO 直接不使能 无力


if __name__ == '__main__':
    main()
