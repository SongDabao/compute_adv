__author__ = 'zhanghao'
import jieba
import jieba.analyse
import os
import math

#读取文件
source="H:\计算广告学\SogouC.reduced\Reduced"
tt=os.walk()
first=tt.__next__()

#('H:\\计算广告学\\SogouC.reduced\\Reduced', ['互联网', '体育', '健康', '军事', '招聘', '教育', '文化', '旅游', '财经'], [])
fature_dict={}
fature_Number=20

#-------------
#     分类方法。用数字表示第几类吧，这样好提取key然后看第一个字符是就知道是第几类了
#-----------


#这个函数从文件夹中读取文件，然后提取特征向量装进dict里面(参数：文件夹内容truple，key的名字也就是分类)
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
            fature_dict[className]=fatureList   # 字典格式 { 'internet' :[ [..] [..] [..] ] }


#这个函数处理数据,产生特征向量
def handleData(data):
    seg=jieba.analyse.extract_tags(data,fature_Number)
    return seg

##---------------------------------------------------有一个问题，就是关于fature怎么读额问题，需要考虑一下，不是不能读，要”优雅“的读

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
 #   ('H:\\计算广告学\\SogouC.reduced\\Reduced', ['互联网', '体育', '健康', '军事', '招聘', '教育', '文化', '旅游', '财经'], [])
 # ("路径名称"，[包含的文件夹名]，[包含的文件名])
"""
#贝叶斯函数
def Byes(target,classname):
    possible=0
    for subword in target:
        possible+=get_pos(subword,classname)
    return possible

#计算一个单词的概率
def get_pos(word,classname):
    SN=0           #SN,记录一共有多少个词
    N=0            #N记录该类有多少个词
    sumcount=0     #该词在全局出现多少次
    count=0        #该词在该类出现多少次
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
#target:待分类的特征向量
#fature_dict 测试集特征集和
'''
     使用m-估计的方法来估计条件概率
     P(x|y)=(nc+m*p)/(n+m)
     在多项式模型中，m=|V|,p=1/|V|
'''
def scan(target,fature_dict):
    count_dict={}
    N=0   #总共多少个词
    V=0   #总共有多少不同的词
    N_class={} #每个类有多少个词
    #初始化 i是待归类文件的特征向量，key是不同的类别
    for i in target:
        for key in fature_dict.keys():
            count_dict[i]={}
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
#---------字典结构{‘待归类文件fature的词’:{'类别':num}}

def Byes(target,classname):
    possible=0
    count_dict=scan(target,fature_dict)
    for subword in target:
        possible*=get_pos(subword,classname)       ##----->是加还是乘？？？？？？？？？？、
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
