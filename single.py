# -*- coding: utf-8 -*-

#单个节点计算

import time

def deal_data1(data):#处理接收的数据,找到最大值，这里可以直接用max()来做
    max=data[0]
    for i in data:
        if max<i:
            max=i
    return max#返回最大值

def is_Coprime(x,y):#判断两个数是否互质
    if x>1 and y>1:
        t=0
        if x<y:
            t=x
            x=y
            y=t
        while x%y:
            t=y
            y=x%y
            x=t
    if y==1:
        return True
    else:
        return False


def deal_data2(data,x):#找到最大与x互质的值
    Max=1
    for i in data:
        if is_Coprime(x,i) and i>Max:
            Max=i
    return Max

def createData():#生成数据集
    data=[]
    for i in range(10000):
        data.append(i+1)
    return data

data=createData()
start = time.time()
max=deal_data1(data)
MaxPrime=deal_data2(data,max)
end =time.time()
print("最大互质数为:",MaxPrime)
print("总用时为:%.2f秒"%(end-start))
#print("")