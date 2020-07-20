[toc]

# ————————————————————————————

# bingo~ 电源选型

## 线性电源

1. 5v 3A 树莓派

2. 5v 330mA 称重模块

   结果：LM317 LM337

## 开关电源

1. LED灯 4.8W/m
2. 2个电机驱动器 24v/2A
3. 至少106W   --- 购买150W



# ————————————————————————————

# 守护进程

1.  [PEP3143](https://www.python.org/dev/peps/pep-3143/)
2. [& 与 nohup区别](https://www.jb51.net/article/172361.htm)
3. [python-daemon](https://pypi.org/project/python-daemon/)

4. [daemon 与 nohup + & 区别](https://blog.csdn.net/lovemdx/article/details/20529563)

## 自己探索

1. 守护进程开启 deamon.py

   ```python
   import daemon
   import test
   
   with daemon.DaemonContext():
       while True:
           test.test()
   ```

2. kill 守护进程

   ```bash
   $ sudo ps -aux | grep deamon
   $ sudo kill xxxx
   ```

   > 自己的电脑会返回到登录界面

3. 目前探索与问题
   - 问：如果kill了守护进程会重启，那么完事大吉。 设置开机启动就可。问：但是守护进程的意义何在？ 目前更多的像在守护内容。
     - 可以试试 拿非死循环试试 
     - 登录后看是否会自再次自启动
   - 解决：

   

   - 目前 树莓派 upgrade的时候内存不够
     - 搜索问题

   

   

   - bingo~目前树莓派 安装python-daemon的时候 timeout
     - 测试网线 是否为网速原因 是的
     - 是否是源的原因 尚未检测





# ————————————————————————————

# 串口

[官方文档](https://www.raspberrypi.org/documentation/configuration/uart.md)

[参考博客](https://blog.csdn.net/ReCclay/article/details/104679944?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase)

## bingo~测试代码

在windows的 hardware的 UART上

## bingo~测试

硬件：串口、杜邦线(母母)、电源5v、树莓派、电脑

1.  bingo~用树莓派的python能发进电脑端来
   1. 用串口模块
   2. 用串口助手
   
2. bingo~树莓派能接收到电脑端的信息，收发一个来回

   1. 用串口模块
   2. 用串口助手

3. bingo~硬件能接收电脑的信息并返回正确的对应测量信息
   1. 串口助手
   2. 串口模块

4. bingo~联调

   树莓派访问，发送信息 然后将接受到的测量信息 print出来。

## bingo~0716

- 接收到的数据

  ```python
  # b'+      0.18 g \r\n'
  ```

- 根据传感器特性 写逻辑
- 处理接受后的数据
  - 拿到数据
  - 处理数据 取值计算结果 和误差

## 整理整个串口过程

1. 调用参数的时候 记住要时时刻刻看参数类型，避免将函数调用成int 特别是类型相近的时候。
2. 今日整理串口部分。

## 目前存在的问题

1. 树莓派如何用另一个包里的东西
   - 做成包，导入包的思想 可测试
   - 能不能打开整个项目。
2. 传感器测量速度慢，回传速度慢。

# ————————————————————————————

# IIC

## 资料

[smbus2 库](https://pypi.org/project/smbus2/)

```bash
# 确保系统为最新的
sudo apt-get update
sudo apt-get upgrade
# 安装python工具
sudo apt-get install python
sudo apt-get install python-dev
sudo apt-get install libjpeg-dev
sudo apt-get install libfreetype6-dev
sudo apt-get install python-setuptools
sudo apt-get install python-pip
sudo apt-get install easy_install
# 如果提示找不到某个包就apt查找一下,替换为正确的名字
sudo apt-cache search 关键字
# 更新Python的库
sudo easy_install -U distribute
# 安装GPIO
sudo pip install RPi.GPIO
sudo pip install pySerial
sudo pip install nose
sudo pip install cmd2
```

## 终端测试

1. 打开树莓派的IIC接口功能 下载工具

```bash
sudo apt-get install i2c-tools python-smbus
```

2. 检测设备

```bash
sudo i2cdetect -y 1
```

3. 读取IIC设备信息

```bash
sudo i2cdump -y 1 0x36 # 0x36为设备号
```

## python测试

```python
import smbus
i2c_bus = smbus.SMBus(1)
slave_addr = 0x36
# Raw Angle(原始角度) 0x0C 0x0D Angle(缩放后的角度) 0x0E 0x0F 
i2c_bus.read_byte_data(slave_addr, 0x0C,4) # 偏移0x0C 读 4个字节 或者2个字节 
```

 ## 下一步

### 计算

1. 计算接收到的数据

   1. 0 1 那么就按位计算角度编码值 angle_code

   2. 计算角度值 angle_code/4096 * 360

   3. **关键点**： 越过360加一圈 $ x=2 $ 

      1. vmax = 5r/s = 1800°/s

      2. 计算 

         ```python
         if (last_angle - angle)/t > 1800:
             circle += 1
         elif (last_angle - angle)/t < - 1800:
             cirle -=1
         # 绝对值角度 初始位置对应的编码值不为零就需要减去初始位置的值init_angle喽 
         absolut_angle = cirle * 360 + angle - init_angle 
         ```

   4. 绝对编码器：告诉我当前的角度(编码值)和方向(DIR的设置和增减确定)。所需要做的就是看 托盘两个极限位置对应的角度值，然后进行后续累加计算。（可以将其中一个极限位置调整到角度为0）

2. 测试

   1. 用中断测试 IIC 设备和设备信息。

   2. 用python 读取对应的角度值。

   3. 将角度值转化。

   4. 写算法 找到对应的 a b c d值就可以了

      S型曲线 y = e/(a+be^(-c(x+d)))

      ```python
      import sympy
      import numpy as np
      
      # y = e/(a+be^(-c(x+d)))
      '''
      a e 决定最大值
      b 会影响中心位置 可以将b等价为 e^n方式
      c 决定陡峭程度
      d 决定中心位置 最大速度对应的位置
      '''
      x = sympy.Symbol('x')
      b = sympy.Symbol('b')
      y = 1 / (1 + np.e ** (-5 * (x - 2)))
      sympy.plot(y, (x, -10, 10))
      sympy.plot((sympy.diff(y, x)), (x, -10, 10))
      print((sympy.diff(y, x)))
      sympy.plot((sympy.diff(sympy.diff(y, x), x)), (x, -10, 10))
      ```

      然后 将v 对应为 y' 注意取值间隔

      