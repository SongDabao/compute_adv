__author__ = 'zhanghao'
'''
source="H:\������ѧ\SogouC.reduced\Reduced"
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
            fature_dict[className]=fatureList   # �ֵ��ʽ { 'internet' :[ [..] [..] [..] ] }

#���������������,������������
def handleData(data):
    seg=jieba.analyse.extract_tags(data,fature_Number)
    return seg

#internet
internet =tt.__next__()
readData(internet,'internet')


print(len(fature_dict['internet']))

#-----------
#������������ǳɹ���
#-----------

####����������㷨ʵ��
#����fature_dict�Ѿ���ȡ��������ʽ��
{'internert': [["","",""],["",""],["","",""],["","",""]],
    'tiyu'  : [["","",""],["",""],["","",""],["","",""]]
}

#a������������°�������ʵ��ĵ�����
#b�����ڸ÷����°�������ʵ��ĵ�����
#c������������²���������ʵ��ĵ�����
#d�����ڸ÷����£��Ҳ���������ʵ��ĵ�����
'''

 #��ʼ�� i�Ǵ������ļ�������������key�ǲ�ͬ�����
   #��ʼɨ��
   ##��֪����ôд�в��У���������ô����˼