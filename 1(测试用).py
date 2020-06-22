import math

def detach(s,n,m):#拆分数据
#s为数据集，n为len(s),m为节点数，k为节点编号,拆分成m份
    num=math.ceil(n/m)#向上取整来拆分
    data= [s[i:i+num] for i in range(0, len(s), num)]
    #生成的拆分列表
    return data#多数据列表

data=[1,2,3,4,5,6,7,9]
max=detach(data,len(data),4)
print(max)