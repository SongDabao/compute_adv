#-*- coding:utf8 -*-
#coding=utf-8
__author__ = 'zhanghao'
import jieba
import jieba.analyse
import os


def scan(target,fature_dict):
    count_dict={}
    N=0
    V=0
    #中文显示
    for i in target:
        #啦啦啦啦
        for key in fature_dict.keys():
            count_dict[i]={}
            count_dict[i][key]=0

    for (k,v) in fature_dict.items():
        for valuse_list in v:
            V+=len(set(valuse_list))
            for valuse in valuse_list:
                N+=1
                if valuse in target:
                    count_dict[valuse][k]+=1
    return (count_dict,N,V)

dica={"fuc","env","than"}
fature={"inter":[["fuc",'you','kes','fuc'],['df','env','sdf'],['than','df','ef']]}
(result,n,v)=scan(dica,fature)
print(result,n,v)










