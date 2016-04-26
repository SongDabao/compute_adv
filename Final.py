#-*- coding:utf8 -*-
#coding=utf-8
__author__ = 'zhanghao'

import jieba
import jieba.analyse
import os
import math


#---------------------------------------预处理阶段--------------------------------------------------#
def readData(source):
    tt=os.walk(source)
    root=tt.__next__()
    fature_dict={}
    for className in root[1]:
        class_dir=tt.__next__()
        fature_dict[className]=getfature(class_dir)
    return fature_dict

def getfature(dir):
    fatureList=[]
    for name in dir[2]:
        fullname=dir[0]+"\\"+name
        #print(fullname)
        with open(fullname,'r') as file:
            try:
                data = file.read()
            except:
                #print("there is an exception")
                continue
            fature=handletargetData(data)   ##-------------------------------事实证明，用handletargetData,比用handleData的正确率要高
            fatureList.append(fature)
    return fatureList
           # fature_dict[className]=fatureList   # 字典格式 { 'internet' :[ [..] [..] [..] ] }
           
#测试集文件，取前30个值
def handletargetData(data):
    seg=jieba.analyse.extract_tags(data,50) #是否采取特征词的方式？？？？
    #应该加上处理步骤，因为得到的特征会有‘&nbsp’这种东西，以及数字，因为好像这个函数会提取数字（整数和浮点数）
    seg=list(seg)
    new_seg=[]
    for seg_i in seg:
        new_seg.append(seg_i)
    for seg_i in seg:
        if  seg_i=='nbsp':
            new_seg.remove(seg_i)
        try:
            float(seg_i)
            new_seg.remove(seg_i)
        except:
            pass
    return new_seg
#训练集文件，取全部值
def handleData(data):   
    seg=jieba.cut(data)
    return list(seg)

def scan(target,fature_dict):
    count_dict={}
    N=0   #总共多少个词
    V=0   #总共有多少不同的词
    N_class={} #每个类有多少个词
    #初始化 i是待归类文件的特征向量，key是不同的类别
    for i in target:
        count_dict[i]={}
        for key in fature_dict.keys():
            count_dict[i][key]=0
    #初始化N_class
    for cls in fature_dict.keys():
        N_class[cls]=0
    #开始扫描
    for (k,v) in fature_dict.items():
        for valuse_list in v:
            V+=len(set(valuse_list))
            N_class[k]+=len(valuse_list)
            for valuse in valuse_list:
                N+=1
                if valuse in target:
                    count_dict[valuse][k]+=1   ##不知道这么写行不行，反正是这么个意思
    #print(N_class,V)
    return (count_dict,N,V,N_class)
#--------------------------------------贝叶斯分类算法实现-----------------------------------------------#

def Byes(target,classname):
    possible=1
    count_dict=scan(target,fature_dict)
    for subword in target:
        possible+=get_pos(subword,classname)       ##----->是加还是乘？？？？？？？？？？、
        #print("possible of ",subword,"is",possible)
    return possible

def get_pos(word,classname):

    Pword_class=(count_dict[word][classname]+1)/(N_class[classname]+V)
    Pclass=1/12
    sumcount=0
    for class_i in count_dict[word].keys():
        sumcount+=count_dict[word][class_i]
    Pword=sumcount/N
    #print(classname,"------->",Pword_class,Pclass,Pword)
    #return (Pword_class*Pclass)/Pword
    return math.log(Pword_class)


def get_target_fature(filepath):

    with open(filepath,'r') as file:
            try:
                data = file.read()
            except:
                print("--------there is an exception")
    target_fature=handletargetData(data)
    #print(target_fature)
    return target_fature
    


if __name__== '__main__':
    zhengqueshu=0
    class_target_name="zhaopin"
    zhonggongshu=0
    
    source="H:\计算广告学\SogouC.reduced\Reduced"
    fature_dict=readData(source)
    targetpath="H:\计算广告学\SogouC.reduced\\test_dir"
    walk=os.walk(targetpath)
    test_root=walk.__next__()
    for test_name in test_root[2]:
        fulltestname=test_root[0]+"\\"+test_name
        print("test_name is==>",fulltestname )
        try:
            target=get_target_fature(fulltestname)
        except:
            print("this file has a problem")
            continue
        (count_dict,N,V,N_class)= scan(target,fature_dict)
        largest=-100000
        result=''
        for a_class in fature_dict.keys():
            tmp=Byes(target,a_class)
            #print("byes of ",a_class,"is",tmp)
            if largest<tmp:
                largest=tmp
                result=str(a_class)
        if result == class_target_name:
            zhengqueshu+=1
        zhonggongshu+=1
        print("结果是----------------->"+result,largest)
    print("正确率是：",(zhengqueshu/zhonggongshu))




#将fature_dict 写入fature_dict.txt
f=open("./fature_dict.txt",'wb')
pickle.dump(fature_dict,f)
f.close()
#把文件重新读回来
f = open('dump.txt', 'rb')
d = pickle.load(f)
f.close()
#
'''
文化 --0.91
财经 -- 0.32
互联网 --0.78
健康 --0.67
教育 -- 0.97     --0.75
军事 -- 0.89
旅游 -- 0.63
体育 --0.84   --0.9
招聘--0.3      --0.52

当吧所有文件都加上之后，招聘的正确率由0.52变成了1.0，也就是全都对

    source="H:\计算广告学\SogouC.reduced\Reduced"
    fature_dict=readData(source)
    target=get_target_fature(targetpath)
    
    (count_dict,N,V,N_class)= scan(target,fature_dict)
    largest=-100000
    result=''
    for a_class in fature_dict.keys():
        tmp=Byes(target,a_class)
        print("byes of ",a_class,"is",tmp)
        if largest<tmp:
            largest=tmp
            result=str(a_class)

    print("最激动而内心的时刻到了...")
    print("结果是----------------->"+result,largest)
'''
