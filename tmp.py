__author__ = 'zhanghao'
'''
source="H:\计算广告学\SogouC.reduced\Reduced"
tt=os.walk(source)
root=tt.__next__()

fature_dict={}
fature_Number=20

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

#internet
internet =tt.__next__()
readData(internet,'internet')


print(len(fature_dict['internet']))

#-----------
#上面这个程序是成功的
#-----------

####卡方检验的算法实现
#假设fature_dict已经提取出来，格式是
{'internert': [["","",""],["",""],["","",""],["","",""]],
    'tiyu'  : [["","",""],["",""],["","",""],["","",""]]
}

#a：在这个分类下包含这个词的文档数量
#b：不在该分类下包含这个词的文档数量
#c：在这个分类下不包含这个词的文档数量
#d：不在该分类下，且不包含这个词的文档数量
'''

 #初始化 i是待归类文件的特征向量，key是不同的类别
   #开始扫描
   ##不知道这么写行不行，反正是这么个意思