import time

def createData():#创建一组数据
    data=[]
    for i in range(1000):#1-1000
        data.append(i+1)
    return data

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



data=createData()

start =time.time()
#print(max(data))
print(deal_data2(data,max(data)))
end =time.time()
print('Running time: %s Seconds'%(end-start))