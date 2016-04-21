__author__ = 'zhanghao'
import jieba
import jieba.analyse
import os
import math

#��ȡ�ļ�
source="H:\������ѧ\SogouC.reduced\Reduced"
tt=os.walk()
first=tt.__next__()

#('H:\\������ѧ\\SogouC.reduced\\Reduced', ['������', '����', '����', '����', '��Ƹ', '����', '�Ļ�', '����', '�ƾ�'], [])
fature_dict={}
fature_Number=20

#-------------
#     ���෽���������ֱ�ʾ�ڼ���ɣ���������ȡkeyȻ�󿴵�һ���ַ��Ǿ�֪���ǵڼ�����
#-----------


#����������ļ����ж�ȡ�ļ���Ȼ����ȡ��������װ��dict����(�������ļ�������truple��key������Ҳ���Ƿ���)
def readData(dir,className):
    fatureList=[]
    for name in dir[2]:
        fullname=dir[0]+"\\"+name
        print(fullname)
        with open(fullname,'r') as file:
            try:
                data = file.read()
            except:
                print("there is an exception")
                continue
            fature=handleData(data)
            fatureList.append(fature)
            fature_dict[className]=fatureList   # �ֵ��ʽ { 'internet' :[ [..] [..] [..] ] }


#���������������,������������
def handleData(data):
    seg=jieba.analyse.extract_tags(data,fature_Number)
    return seg

##---------------------------------------------------��һ�����⣬���ǹ���fature��ô�������⣬��Ҫ����һ�£����ǲ��ܶ���Ҫ�����š��Ķ�

internet =tt.__next__()
readData(internet,'1')
tiyu =tt.__next__()
readData(tiyu,'2')
jiankang=tt.__next__()
readData(jiankang,'')
zhaopin=tt.__next__()
readData(zhaopin,'4')
jiaoyu=tt.__next__()
readData(jiaoyu,'5')
wenhua=tt.__next__()
readData(wenhua,'6')
lvyou=tt.__next__()
readData(lvyou,'7')
caijing=tt.__next__()
readData(caijing,'8')

#    ------------------------------------------------
 #   ('H:\\������ѧ\\SogouC.reduced\\Reduced', ['������', '����', '����', '����', '��Ƹ', '����', '�Ļ�', '����', '�ƾ�'], [])
 # ("·������"��[�������ļ�����]��[�������ļ���])
"""
#��Ҷ˹����
def Byes(target,classname):
    possible=0
    for subword in target:
        possible+=get_pos(subword,classname)
    return possible

#����һ�����ʵĸ���
def get_pos(word,classname):
    SN=0           #SN,��¼һ���ж��ٸ���
    N=0            #N��¼�����ж��ٸ���
    sumcount=0     #�ô���ȫ�ֳ��ֶ��ٴ�
    count=0        #�ô��ڸ�����ֶ��ٴ�
    for (k,v) in fature_dict.items():
        SN+=len(v)
        if str(k)==classname:
            N+=len(v)
            if word in v:
                count+=1
                sumcount+=1
        else:
            if word in v:
                sumcount+=1
    Pword_class=count/N
    Pclass=len(fature_dict)
    Pword=sumcount/SN
    return (Pword_class*Pclass)/Pword

"""
#target:���������������
#fature_dict ���Լ���������
'''
     ʹ��m-���Ƶķ�����������������
     P(x|y)=(nc+m*p)/(n+m)
     �ڶ���ʽģ���У�m=|V|,p=1/|V|
'''
def scan(target,fature_dict):
    count_dict={}
    N=0   #�ܹ����ٸ���
    V=0   #�ܹ��ж��ٲ�ͬ�Ĵ�
    N_class={} #ÿ�����ж��ٸ���
    #��ʼ�� i�Ǵ������ļ�������������key�ǲ�ͬ�����
    for i in target:
        for key in fature_dict.keys():
            count_dict[i]={}
            count_dict[i][key]=0
    #��ʼ��N_class
    for cls in fature_dict.keys():
        N_class[cls]=0
    #��ʼɨ��
    for (k,v) in fature_dict.items():
        for valuse_list in v:
            V+=len(set(valuse_list))
            N_class[k]+=len(valuse_list)
            for valuse in valuse_list:
                N+=1
                if valuse in target:
                    count_dict[valuse][k]+=1   ##��֪����ôд�в��У���������ô����˼
    return (count_dict,N,V,N_class)
#---------�ֵ�ṹ{���������ļ�fature�Ĵʡ�:{'���':num}}

def Byes(target,classname):
    possible=0
    count_dict=scan(target,fature_dict)
    for subword in target:
        possible*=get_pos(subword,classname)       ##----->�Ǽӻ��ǳˣ���������������������
    return math.log(possible)

target=[]
count_dict={}
N=0
(count_dict,N,V,N_class)=scan(target,fature_dict)

def get_pos(word,classname):

    Pword_class=(count_dict[word][classname]+1)/N_class[classname]+V
    Pclass=1/12
    sumcount=0
    for class_i in count_dict[word].keys():
        sumcount+=count_dict[word][class_i]
    Pword=sumcount/N
    return (Pword_class*Pclass)/Pword


def get_target_fature(filepath):

    with open(filepath,'r') as file:
            try:
                data = file.read()
            except:
                print("there is an exception")
    return handleData(data)


if __name__=="main":
    fature_dict={}
    count_dict={}
    classes=['internet','tiyu','jiankang','zhaopin','jiaoyu','wenhua','lvyou','caijing','caijing']
    filepath=''
    classname=''
    po={}
    fature_dict_g=readData(dir,classname)
    target=get_target_fature(filepath)
    for classname2 in classes:
        po[classname2]=Byes(target,classname)
    result=sorted(dict.items(), key=lambda d: d[1])
    print(result)
