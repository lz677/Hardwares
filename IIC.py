#! C:\Users\93715\Anaconda3\python.exe
# *-* coding:utf8 *-*
"""
@author: LiuZhe
@license: (C) Copyright SJTU ME
@contact: LiuZhe_54677@sjtu.edu.cn
@file: IIC.py
@time: 2020/7/13 19:17
@desc: LESS IS MORE
"""
import sympy
import numpy as np
import time

# try:
#     from smbus2 import SMBus
# except RuntimeError:
#     print("please install smbus")


# y = 1/(a+be^(-c(x+d)))
'''
a 决定最大值
b 会影响中心位置 可以将b等价为 e^n方式
c 决定陡峭程度
d 决定中心位置 最大速度对应的位置
'''
phi_max = 3600
t = sympy.Symbol('t')
v_const = 1800
t_max = phi_max / v_const
phi = v_const * t
c = 4
d = -0.2
a = phi_max * (1 + np.e ** ((-c) * (t_max / 2 + d))) * (1 + np.e ** (c * (t_max / 2 + d))) / (
        (1 + np.e ** (c * (t_max / 2 + d))) - (1 + np.e ** ((-c) * (t_max / 2 + d))))
b = - a / (1 + np.e ** (c * (t_max / 2 + d)))
phi_app = a / (1 + np.e ** (-c * (t - (t_max / 2 + d)))) + b
sympy.plot(phi, phi_app, (t, 0, t_max + 0.2))
v_app = sympy.diff(phi_app)
print(phi_app)
print(v_app)
sympy.plot(sympy.diff(phi), v_app, (t, 0, t_max + 0.2))
phi_cal = sympy.Symbol('phi')
v_cal = 4 * (phi_cal + 152.9797250804)*(3905.9594501608 - phi_cal - 152.9797250804) / 3905.9594501608
fre_cal = v_cal/360 * 1600
sympy.plot(fre_cal, (phi_cal, 0, phi_max))


# x = sympy.Symbol('x')
# b = sympy.Symbol('b')
# y = 1 / (1 + np.e ** (-5 * (x - 2)))
# sympy.plot(y, (x, -1, 10))
# sympy.plot((sympy.diff(y, x)), (x, -1, 10))
# print((sympy.diff(y, x)))
# sympy.plot((sympy.diff(sympy.diff(y, x), x)), (x, -1, 10))

# slave_addr = 0x36
# start = 95
# angle, last_angle, circle = start, start, 0
# t = 1
# try:
#     with SMBus(1) as i2c_bus:
#         while True:
#             a = i2c_bus.read_byte_data(slave_addr, 0x0C)  # 偏移0x0C 读 4个字节 或者2个字节
#             b = i2c_bus.read_byte_data(slave_addr, 0x0D)
#             c = (a << 8) + b
#             angle = c / 4096 * 360
#             if (last_angle - angle) / t > 180:
#                 circle += 1
#             elif (last_angle - angle) / t < - 180:
#                 circle -= 1
#             last_angle = angle
#             print('angle:', c / 4096 * 360)
#             print('circle:', circle)
#             print('total', int(c / 4096 * 360 + circle * 360 - start))
#             time.sleep(1)
# except KeyboardInterrupt:
#     i2c_bus.close()
#     print('程序终止')
