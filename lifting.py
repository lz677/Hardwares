#! C:\Users\93715\Anaconda3\python.exe
# *-* coding:utf8 *-*
"""
@author: LiuZhe
@license: (C) Copyright SJTU ME
@contact: LiuZhe_54677@sjtu.edu.cn
@file: lifting.py
@time: 2020/7/4 16:19
@desc: LESS IS MORE
"""
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("没有成功导入包：RPi.GPIO")

"""
控制逻辑：
    1.开机初始化 电机顺时针初始化至初始状态 慢速
    2.接触到行程开关停止电机旋转
        此时电机的状态：disable or 继电器断电
        需要测试：
"""
GPIO.setmode(GPIO.BOARD)  # 编号方式采用BOARD

pin_COM = 32  # COM 3.3-5v 采用共阳极
pin_DIR = 36  # DIR direction 方向信号 0V Vcom
pin_STP = 38  # STP 步进信号 100-20KHz
pin_EN = 40  # 脱机信号 Vcom使能电机 0V步进电机脱机状态
pins = (32, 36, 38, 40)

pin_NC = 7  # NC: pin13
pin_NO = 11  # NO: pin15

pin_NC_close_lifting = 13  # NC: pin7
pin_NO_close_lifting = 15  # NO: pin11
# pins_travel_switch = (7, 11)
pins_travel_switch = (7, 11, 13, 15)

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


def test(first_flag: bool, close_flag: bool, pwm_tran):
    # enable_or_disable(False)
    # 测试行程开关
    if GPIO.input(pin_NC_close_lifting) == 1 or GPIO.input(pin_NO_close_lifting) == 0:
        print("正在初始化抬升...") if first_flag else None
        enable_or_disable(True)
        pwm.ChangeDutyCycle(50)

    elif GPIO.input(pin_NO_close_lifting) == 1 and GPIO.input(pin_NC_close_lifting) == 0:
        pwm.ChangeDutyCycle(0)
        print("已初始化完成") if not close_flag else None
        close_flag = True
    return close_flag


if __name__ == '__main__':
    print("测试开始...")
    init()
    cw_or_ccw(False)
    pwm = GPIO.PWM(pin_STP, 800)  # 初始化PWM实例 频率为100-20kHz 1600 -> 1r/s
    pwm.start(0)  # 开始脉宽调制，参数范围为0->100
    o_first_flag = True
    cl_flag = False
    try:
        if GPIO.input(pin_NO_close_lifting) == 1 and GPIO.input(pin_NC_close_lifting) == 0:
            time.sleep(5)
            if GPIO.input(pin_NO_close_lifting) == 1 and GPIO.input(pin_NC_close_lifting) == 0:
                enable_or_disable(False)
                print("正处于初试状态，初始化完毕")
            else:
                while True:
                    if not cl_flag:
                        cl_flag = test(o_first_flag, cl_flag, pwm)
                        o_first_flag = False
                    else:
                        break
        else:
            while True:
                if not cl_flag:
                    cl_flag = test(o_first_flag, cl_flag, pwm)
                    o_first_flag = False
                else:
                    break
        print("测试结束")
        clearup()  # 清空GPIO
    except KeyboardInterrupt:
        print("程序被中断")
        clearup()  # 清空GPIO
