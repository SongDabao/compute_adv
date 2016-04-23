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
                print("there is an exception")
                continue
            fature=handleData(data)
            fatureList.append(fature)
    return fatureList
           # fature_dict[className]=fatureList   # 字典格式 { 'internet' :[ [..] [..] [..] ] }

def handleData(data):
    #seg=jieba.analyse.extract_tags(data,20) #是否采取特征词的方式？？？？
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
    return (count_dict,N,V,N_class)
#--------------------------------------贝叶斯分类算法实现-----------------------------------------------#

def Byes(target,classname):
    possible=0
    count_dict=scan(target,fature_dict)
    for subword in target:
        possible*=get_pos(subword,classname)       ##----->是加还是乘？？？？？？？？？？、
    return math.log(possible)

def get_pos(word,classname):

    Pword_class=(count_dict[word][classname]+1)/(N_class[classname]+V)
    Pclass=1/12
    sumcount=0
    for class_i in count_dict[word].keys():
        sumcount+=count_dict[word][class_i]
    Pword=sumcount/N
    print(classname,"------->",Pword_class,Pclass,Pword)
    return (Pword_class*Pclass)/Pword


def get_target_fature(filepath):

    with open(filepath,'r') as file:
            try:
                data = file.read()
            except:
                print("--------there is an exception")
    print(data)
    target_fature=handleData(data)
    return target_fature


if __name__== '__main__':
    source="H:\计算广告学\SogouC.reduced\Reduced"
    targetpath="H:\\计算广告学\\SogouC.reduced\\44.txt"
    fature_dict=readData(source)
    target=get_target_fature(targetpath)
    
    (count_dict,N,V,N_class)= scan(target,fature_dict)
    largest=0.00
    result=''
    for a_class in fature_dict.keys():
        tmp=Byes(target,a_class)
        if larget<tmp:
            larget=tmp
            result=a_class

    print("最激动而内心的时刻到了...")
    print("结果是----------------->"+result)


