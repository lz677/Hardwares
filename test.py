#! C:\Users\93715\Anaconda3\python.exe
# *-* coding:utf8 *-*
"""
@author: LiuZhe
@license: (C) Copyright SJTU ME
@contact: LiuZhe_54677@sjtu.edu.cn
@file: test.py
@time: 2020/7/5 19:27
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
# 抽屉电机
pin_drawer_COM = 32  # COM 3.3-5v 采用共阳极
pin_drawer_DIR = 36  # DIR direction 方向信号 0V Vcom
pin_drawer_STP = 38  # STP 步进信号 100-20KHz
pin_drawer_EN = 40  # 脱机信号 Vcom使能电机 0V步进电机脱机状态

# 抬升电机
pin_COM = 31  # COM 3.3-5v 采用共阳极
pin_DIR = 33  # DIR direction 方向信号 0V Vcom
pin_STP = 35  # STP 步进信号 100-20KHz
pin_EN = 37  # 脱机信号 Vcom使能电机 0V步进电机脱机状态
pins = (31, 33, 35, 37, 32, 36, 38, 40)

# 行程开关
# 抽屉关闭位置
pin_NC_close_drawer = 7  # NC: pin7
pin_NO_close_drawer = 11  # NO: pin11
# 抽屉打开位置
pin_NC_open_drawer = 13  # NC: pin13
pin_NO_open_drawer = 15  # NO: pin15

# 抬升初始位置
pin_NC_up_lifting = 12  # NC: pin12
pin_NO_up_lifting = 16  # NO: pin16

# 抬升终止位置
pin_NC_down_lifting = 18  # NC: pin18
pin_NO_down_lifting = 22  # NO: pin22
# pins_travel_switch = (7, 11, 13, 15, 12, 16, 18, 22)
pins_travel_switch = (7, 11, 13, 15, 12, 16, 18, 22)
dr = 'drawer'
lf = 'lifting'
# 初始化GPIO的模式
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)  # 将引脚均设置为输出模式

for pin in pins_travel_switch:
    GPIO.setup(pin, GPIO.IN)


# 初始化电机的状态
def init():
    GPIO.output(pin_drawer_COM, True)
    GPIO.output(pin_drawer_DIR, True)
    GPIO.output(pin_drawer_STP, False)
    GPIO.output(pin_drawer_EN, False)
    GPIO.output(pin_COM, True)
    GPIO.output(pin_DIR, True)
    GPIO.output(pin_STP, False)
    GPIO.output(pin_EN, False)


def enable_drawer_motor(is_enable: bool):
    # 抽屉电机使能的时候 抬升电机不使能
    # 允许都不使能

    if is_enable:
        GPIO.output(pin_drawer_EN, is_enable)
        GPIO.output(pin_EN, not is_enable)
    else:
        GPIO.output(pin_drawer_EN, is_enable)


def enable_motor(is_enable: bool, which_motor: str):
    if which_motor == dr:
        if is_enable:
            GPIO.output(pin_drawer_EN, is_enable)
            GPIO.output(pin_EN, not is_enable)
        else:
            GPIO.output(pin_drawer_EN, is_enable)
    elif which_motor == lf:
        if is_enable:
            GPIO.output(pin_EN, is_enable)
            GPIO.output(pin_drawer_EN, not is_enable)
        else:
            GPIO.output(pin_EN, is_enable)
    else:
        print('没有对应的电机被使能')


def cw_or_ccw(is_cw: bool, is_drawer: bool):
    if is_drawer:
        GPIO.output(pin_drawer_DIR, is_cw)
    else:
        GPIO.output(pin_DIR, is_cw)


def clean_up():
    GPIO.cleanup()  # 清楚引用引脚


def motor(is_close: bool, pwm, which_motor: str):
    enable_motor(True, which_motor)
    while True:
        if which_motor == dr:
            if is_close and GPIO.input(pin_NO_close_drawer) and not GPIO.input(pin_NC_close_drawer):
                break
            elif not is_close and GPIO.input(pin_NO_open_drawer) and not GPIO.input(pin_NC_open_drawer):
                break
            else:
                # 旋转
                cw_or_ccw(True, True) if is_close else cw_or_ccw(False, True)
                # print("1", end='')
                pwm.ChangeDutyCycle(10)
        elif which_motor == lf:
            if is_close and GPIO.input(pin_NO_up_lifting) and not GPIO.input(pin_NC_up_lifting):
                break
            elif not is_close and GPIO.input(pin_NO_down_lifting) and not GPIO.input(pin_NC_down_lifting):
                break
            else:
                # 旋转
                cw_or_ccw(True, False) if is_close else cw_or_ccw(False, False)
                # print("1", end='')
                pwm.ChangeDutyCycle(10)
        else:
            print("没有对应的电机")


def drawer_status(is_init: bool, is_close: bool, pwm, which_motor: str):
    if is_init:
        print("正在初始化 %s......" % which_motor)
        if GPIO.input(pin_NO_close_drawer) and not GPIO.input(pin_NC_close_drawer):
            time.sleep(0.5)
            if GPIO.input(pin_NO_close_drawer) and not GPIO.input(pin_NC_close_drawer):
                enable_motor(False, which_motor)
                print("%s 初始化完毕" % which_motor)
            else:
                motor(True, pwm, which_motor)
                enable_motor(False, which_motor)
                print("\n%s 初始化完成" % which_motor)
        else:
            motor(True, pwm, which_motor)
            enable_motor(False, which_motor)
            print("\n%s 初始化完成" % which_motor)
    else:
        if is_close:
            print("正在关闭 %s" % which_motor)
            motor(True, pwm, which_motor)
            enable_motor(False, which_motor)
            print("\n%s 关闭完成" % which_motor)
        else:
            print("正在打开 %s" % which_motor)
            motor(False, pwm, which_motor)
            enable_motor(False, which_motor)
            print("\n%s 打开完成" % which_motor)


def lifting_status(is_init: bool, is_close: bool, pwm, which_motor: str):
    if is_init:
        print("正在初始化 %s......" % which_motor)
        if GPIO.input(pin_NO_up_lifting) and not GPIO.input(pin_NC_up_lifting):
            time.sleep(0.5)
            if GPIO.input(pin_NO_up_lifting) and not GPIO.input(pin_NC_up_lifting):
                enable_motor(False, which_motor)
                print("%s 初始化完毕" % which_motor)
            else:
                motor(True, pwm, which_motor)
                enable_motor(False, which_motor)
                print("\n%s 初始化完成" % which_motor)
        else:
            motor(True, pwm, which_motor)
            enable_motor(False, which_motor)
            print("\n%s 初始化完成" % which_motor)
    else:
        if is_close:
            print("正在抬升 %s" % which_motor)
            motor(True, pwm, which_motor)
            enable_motor(False, which_motor)
            print("\n%s 抬升完成" % which_motor)
        else:
            print("正在下降 %s" % which_motor)
            motor(False, pwm, which_motor)
            enable_motor(False, which_motor)
            print("\n%s 下降完成" % which_motor)


def main():
    print("程序开始......")
    init()
    pwm_drawer = GPIO.PWM(pin_drawer_STP, 4800)  # 初始化PWM实例 频率为100-20kHz 1600 -> 1r/s
    pwm_drawer.start(0)  # 开始脉宽调制，参数范围为0->100
    pwm_lifting = GPIO.PWM(pin_STP, 800)  # 初始化PWM实例 频率为100-20kHz 1600 -> 1r/s
    pwm_lifting.start(0)  # 开始脉宽调制，参数范围为0->100
    try:
        print("初始化抽屉 等待3s")
        time.sleep(3)
        drawer_status(True, True, pwm_drawer, dr)

        print('\n')
        print("初始化抬升 等待3s")
        print('\n')
        time.sleep(3)
        lifting_status(True, True, pwm_lifting, lf)

        print('\n')
        print("抽屉测试开始 等待3s")
        print('\n')
        time.sleep(3)
        drawer_status(False, False, pwm_drawer, dr)

        print('\n')
        time.sleep(3)
        drawer_status(False, True, pwm_drawer, dr)
        print("抽屉测试结束")

        print('\n')
        print("抬升测试开始 等待3s")
        print('\n')
        time.sleep(3)
        lifting_status(False, False, pwm_lifting, lf)
        print('\n')
        time.sleep(3)
        lifting_status(False, True, pwm_lifting, lf)
        print("抬升测试结束")

        clean_up()
        print('\n')
        print('测试结束')
    except KeyboardInterrupt:
        print("程序被外部中断")
        clean_up()


def test():
    with open('./log.txt', "a+") as f:
        f.write('test')
        time.sleep(5)


if __name__ == '__main__':
    main()
