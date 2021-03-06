# 太极图形课S1 hw2 弹性双摆

## 背景介绍

在双摆的基础下把把原本的连接质点的刚性杆变成了轻弹簧,所以没办法在再像双摆那样仅使用两个广义坐标就描述系统位形.但是这样也使得问题简化,通过弹簧质点法就能求出双摆的加速度,从而模拟双摆的运动.



## 成功效果展示

N = 3

![elastic pendulums](./data/elastic_3.gif)

N = 5

![elastic pendulums](./data/elastic_5.gif)

N = 100

![elastic pendulums](./data/elastic_100.gif)

Tip: 不要把杨氏模量调得太大,否则质点在经过一些极值点的时候能量突变, 双摆系统会炸掉

## 运行方式

`python3 elastic_double_pendulums.py`