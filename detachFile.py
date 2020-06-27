import sys,math

def detachFile(num,filename,lineNum):#拆分文件
    #拆分的份数，文件名,文件行数
    #按行数拆分，条件是数据得均匀
    flag=0#计算行数
   # dataList=[]
    F=open(filename,"r")
    smallFileLine=math.floor(lineNum/num)#一份文件的长度,向上取整
    #print(smallFileLine)

    DirPath=[]
    for i in range(num):
        dirpath="/home/wj/桌面/final/splitData"+str(i)+".txt"#切分后的文件名
        DirPath.append(dirpath)#文件名列表

    ｉ=0
    for line in F.readlines():#读一行
        if flag==0:#根据flag来打开文件
            f=open(DirPath[i],"w")#打开子文件
        if flag<smallFileLine:       
            if i<num-1:
                flag+=1
                f.writelines(line)
                if flag==smallFileLine:#如果到了数据量
                    #flag=0#重新赋值为0
                    flag=0
                    i+=1#重新打开文件
            else:
                f.writelines(line)
                flag+=1
    
filename="/home/wj/桌面/final/data.txt"
num=4
lineNum=100000
detachFile(num,filename,lineNum)