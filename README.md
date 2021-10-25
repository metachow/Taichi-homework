# 太极图形课S1-hw1-双摆(Double Pendulum)
利用taichi的并行特性实现了多个双摆同时起摆,每个双摆之间的起始位置偏移极小.

## 背景简介
> 双摆是将一根单摆连接在另一个单摆的尾部所构成的系统。双摆同时拥有着简单的构造和复杂的行为。高能量双摆的摆动轨迹表现出对于初始状态的极端敏感。

--Wikipedia

双摆的基本结构如图
![double pendulum](./data/dbl_pendulum.gif)


## 成功效果展示
图中分别展示了当双摆的起始位置约为(pi, pi),以及(pi/2, pi/2)时,100个双摆同时开始运动的情况,每个双摆间的角度差为(0, 0.0001),经过一定时间后,位置几乎相同的双摆间的运动轨迹也会发散

![pendulum pi](./data/pendulum-pi.gif)
![pendulim pi/2](./data/pendulum-0.5pi.gif)

## 运行方式

 `python3 double_pendulum.py`
