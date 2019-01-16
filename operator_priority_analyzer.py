import numpy as np
import grammar_copy

Vn={}
Vn_new={}
find=np.ones(1000,dtype=np.int)
key_reflection={}
Vt=[]
First={}
Last={}
Visit=[]
priority_table=None
result_stack=[]
raw_stack=[]
run_flag=True
result_str=''
process_log=[]

class Grammer:
    def __init__(self,str):
        self.left=str
        self.right=[]

    def insert(self,str):
        self.right.append(str)
    def get(self):
        str=self.left+'->'
        for item in self.right:
            str=str+item+'|'
        return str[:-1]

def construct_dict(input_str):
    '''
    建立字典Vn，用来存放每个vn和其对应的Grammer对象
    :param input_str: 传入的文法
    '''
    global Vn,Vt
    input = input_str.split('\n')
    input_grammers = input[:]
    for i in range(len(input_grammers)):
        input_grammer = input_grammers[i]
        str1, str2 = input_grammer.split('->')
        if str1 not in Vn.keys():
            grammer = Grammer(str1)
            grammer.insert(str2)
            Vn[str1] = grammer
        else:
            Vn[str1].insert(str2)
        for char in str2:
            if char not in Vt and not char.isupper():
                Vt.append(char)

def dfs_first(x):
    global Visit,Vn,Vt,First
    if Visit[x]==1:
        return
    Visit[x]=1
    vn=list(Vn.keys())[x]
    grammer=Vn[vn]
    for i in range(len(grammer.right)):
        if grammer.right[i][0].isupper():
            if grammer.right[i].__len__() > 1 and not grammer.right[i][1].isupper():
                First[vn].append(grammer.right[i][1])
            x_=0
            for k,value in enumerate(Vn):
                if grammer.right[i][0]==value:
                    x_=k
                    break
            dfs_first(x_)
            for first_item in First[list(Vn.keys())[x_]]:
                if first_item not in First[vn]:
                    First[vn].append(first_item)
        else:
            First[vn].append(grammer.right[i][0])


def creat_first():
    '''
    创建每个vn的First集
    '''
    global Vn,Visit,First
    num=len(Vn)
    Visit=[0]*num
    for key in Vn.keys():
        First[key]=[]
    for i in range(num):
        if Visit[i]==0:
            dfs_first(i)

def dfs_last(x):
    global Visit, Vn, Vt, Last,First,Last
    if Visit[x] == 1:
        return
    Visit[x] = 1
    vn = list(Vn.keys())[x]
    grammer = Vn[vn]
    for i in range(len(grammer.right)):
        if grammer.right[i][-1].isupper():
            if grammer.right[i].__len__() > 1 and not grammer.right[i][-2].isupper():
                Last[vn].append(grammer.right[i][-2])
            x_ = 0
            for k, value in enumerate(Vn):
                if grammer.right[i][-1] == value:
                    x_ = k
                    break
            dfs_last(x_)
            for last_item in Last[list(Vn.keys())[x_]]:
                if last_item not in Last[vn]:
                    Last[vn].append(last_item)
        else:
            Last[vn].append(grammer.right[i][-1])


def creat_last():
    '''
    创建每个vn的Last集
    '''
    global Vn,Visit,Last
    num=len(Vn)
    Visit=[0]*num
    for key in Vn.keys():
        Last[key]=[]
    for i in range(num):
        if Visit[i]==0:
            dfs_last(i)

def create_table():
    '''
    创建算符优先关系表
    '''
    global priority_table,Vn,Vt
    num=len(Vt)
    priority_table=np.ones((num,num))
    priority_table[:,:]=2
    Vn_len=len(Vn)
    Vn_list=list(Vn.keys())
    for i in range(Vn_len):
        grammer=Vn[Vn_list[i]]
        for j in range(len(grammer.right)):
            str_len=len(grammer.right[j])
            str=grammer.right[j]
            for k in range(str_len-1):
                if (not str[k].isupper()) and (not str[k+1].isupper()):
                    priority_table[Vt.index(str[k]),Vt.index(str[k+1])]=0
                if (not str[k].isupper()) and str[k+1].isupper():
                    for char in First[str[k+1]]:
                        priority_table[Vt.index(str[k]), Vt.index(char)] = -1
                if str[k].isupper() and (not str[k+1].isupper()):
                    for char in Last[str[k]]:
                        priority_table[Vt.index(char), Vt.index(str[k+1])] = 1
                if k+2<str_len and (not str[k].isupper()) and (not str[k+2].isupper()) and str[k+1].isupper():
                    priority_table[Vt.index(str[k]),Vt.index(str[k+2])]=0


def init_find():
    '''
    初始化find数组，将各处的值等于其索引
    '''
    global find,Vn,Vn_new,key_reflection
    for i in range(find.shape[0]):
        find[i]=i
    for key in Vn.keys():
        for right in Vn[key].right:
            if len(right)==1 and right.isupper():
                find[ord(right)]=ord(key)
    Vn_new=grammar_copy.deepcopy(Vn)
    for key in Vn_new.keys():
        for right in Vn_new[key].right:
            right_old=right
            if len(right) == 1 and right.isupper():
                while find[ord(right)]!=ord(right):
                    right=chr(find[ord(right)])
                value=ord(right)
                key_reflection[right_old]=right
    for key in Vn_new.keys():
        for right_index in range(len(Vn_new[key].right)):
            for index in range(len(Vn_new[key].right[right_index])):
                if Vn_new[key].right[right_index][index] in key_reflection.keys():
                    Vn_new[key].right[right_index]=Vn_new[key].right[right_index][:index]+key_reflection[Vn_new[key].right[right_index][index]]+Vn_new[key].right[right_index][index+1:]


def is_exist_vt():
    '''
    判断结果栈中是否存在vt
    :return:返回是否存在和最右边的一个vt
    '''
    global Vn,Vt,priority_table,raw_stack,result_stack
    for item in result_stack[:0:-1]:
        if item in Vt:
            return True,item
    return False,None


def reduction():
    '''
    进行归约的函数
    '''
    global Vn, Vt, priority_table, raw_stack, result_stack,key_reflection,Vn_new
    result_len=len(result_stack)
    end=0
    last_vt=''
    last_index=0
    for i in range(1,result_len):
        if result_stack[i].isupper():
            continue
        if last_vt=='' or priority_table[Vt.index(last_vt),Vt.index(result_stack[i])]<1:
            last_vt=result_stack[i]
            last_index=i
            continue
        if priority_table[Vt.index(last_vt),Vt.index(result_stack[i])]==1:
            end=last_index
            break
        if priority_table[Vt.index(last_vt),Vt.index(result_stack[i])]==2:
            error()
            break
    if end==0 and last_index!=0:
        end=last_index
    str=result_stack[end]
    begin=end-1
    while(begin>0):
        if result_stack[begin].isupper():
            str = result_stack[begin] + str
            begin-=1
            continue
        if priority_table[Vt.index(result_stack[begin]),Vt.index(result_stack[end])]!=0:
            begin+=1
            break
        str=result_stack[begin]+str
        begin-=1
    if begin==0:
        begin+=1
    if begin-1>0 and result_stack[begin-1].isupper():
        str=result_stack[begin-1]+str
        begin-=1
    if end+1<result_len and result_stack[end+1].isupper():
        str=str+result_stack[end+1]
        end+=1
    vn=None
    for index in range(len(str)):
        if str[index] in key_reflection.keys():
            str=str[:index]+key_reflection[str[index]]+str[index+1:]
    for key in Vn_new.keys():
        for right in Vn_new[key].right:
            if right==str:
                vn=key
                break
        if vn!=None:
            break
    if vn==None:
        error()
        return
    result_stack[begin]=vn
    begin_now=begin+1
    end_now=end+1
    while(end_now<result_len):
        result_stack[begin_now]=result_stack[end_now]
        begin_now+=1
        end_now+=1
    while(result_len>begin_now):
        result_stack.pop()
        result_len-=1



def error():
    '''
    生成错误
    '''
    global run_flag
    run_flag=False
    print("Error!")


def calculate(str_list):
    '''
    给定一个list，将其转化为字符串
    :param str_list: 列表
    :return: 转化之后的字符串
    '''
    str=''
    for i in str_list:
        str+=i
    return str

def analyse(input_str):
    '''
    语法分析操作
    :param input_str: 需要进行判断的句子
    '''
    global Vn,Vt,priority_table,raw_stack,result_stack,run_flag,process_log
    for char in input_str[::-1]:
        raw_stack.append(char)
    result_stack.append('#')
    if len(raw_stack)>0:
        top=raw_stack.pop()
    while(True):
        if not run_flag:
            break
        if top.isupper():
            result_stack.append(top)
            if len(raw_stack)==0:break
            top=raw_stack.pop()
            continue
        flag,char=is_exist_vt()
        if not flag:
            log_now = []
            log_now.append(calculate(result_stack)[1:])
            log_now.append('<')
            log_now.append(top)
            log_now.append(calculate(raw_stack))
            if log_now[1]=='<':
                log_now.append('移进')
            elif log_now[1]=='>':
                log_now.append('归约')
            process_log.append(log_now)
            result_stack.append(top)
            if len(raw_stack) == 0: break
            top=raw_stack.pop()
        else:
            if top in Vt and  priority_table[Vt.index(char),Vt.index(top)]<=0:
                log_now = []
                log_now.append(calculate(result_stack)[1:])
                log_now.append(get_symbol(priority_table[Vt.index(char), Vt.index(top)]))
                log_now.append(top)
                log_now.append(calculate(raw_stack))
                if log_now[1] == '<':
                    log_now.append('移进')
                elif log_now[1] == '>':
                    log_now.append('归约')
                process_log.append(log_now)
                result_stack.append(top)
                if len(raw_stack) == 0: break
                top = raw_stack.pop()
            elif top in Vt and  priority_table[Vt.index(char),Vt.index(top)]==1:
                reduction()
            else:
                error()
    flag,char=is_exist_vt()
    log_now = []
    log_now.append(calculate(result_stack)[1:])
    log_now.append('')
    log_now.append('')
    log_now.append(calculate(raw_stack))
    log_now.append('归约')
    process_log.append(log_now)
    while flag:
        if not run_flag:
            break
        reduction()
        flag,char=is_exist_vt()
    if run_flag:
        log_now = []
        log_now.append(calculate(result_stack)[1:])
        log_now.append('')
        log_now.append('')
        log_now.append(calculate(raw_stack))
        log_now.append('')
        process_log.append(log_now)
        print("Successful!")

def get_symbol(x):
    '''
    进行转化，由于在算符优先关系表中存储的是数字，所以通过传入数字转化为比较符
    :param x: 数字
    :return: 比较符
    '''
    if x==0:
        return '='
    elif x==-1:
        return '<'
    elif x==1:
        return '>'
    else:
        return ' '

def create_str():
    '''
    生成准备步骤的字符串
    '''
    global Vn_new, Vn, result_str, Vt,First,Last,priority_table
    result_str += "******************VT集******************\n"
    for vt in Vt:
        result_str += '%s     '%vt
    result_str += '\n*****************产生式*****************\n'
    for key in Vn.keys():
        result_str=result_str+key+'->'
        for right in Vn[key].right:
            result_str=result_str+right+'|'
        result_str=result_str[:-1]+'\n'
    result_str+="****************************************\n"
    result_str+='---------------FIRSTVT集----------------\n'
    for key in First.keys():
        result_str+='%s :'%key
        for i in First[key]:
            result_str+=' %s'%i
        result_str+='\n'
    result_str += '----------------LASTVT集----------------\n'
    for key in Last.keys():
        result_str+='%s :'%key
        for i in Last[key]:
            result_str+=' %s'%i
        result_str+='\n'
    result_str += '----------------算符优先关系表----------------\n'
    result_str+='    '
    for vt in Vt:
        result_str += '%s   '%vt
    result_str+='\n'
    for i in range(len(Vt)):
        result_str+=Vt[i]
        for j in range(len(Vt)):
            result_str+='   %s'%get_symbol(priority_table[i][j])
        result_str+='\n'
    result_str+='---------------------------------------------\n'



def operator_priority_analyse(input_grammer,input_str):
    '''
    :param input_grammer: 输入的语法
    :param input_str: 输入的需要被验证的句子
    :return: 语句是否符合语法，准备步骤生成的字符串，操作过程生成list(里面存储着每次操作的各种信息，为n*5矩阵)
    '''
    global  Vn,Vn_new,find,key_reflection,Vt,First,Last,Visit,priority_table,result_stack,raw_stack,run_flag,result_str,process_log

    Vn = {}
    Vn_new = {}
    find = np.ones(1000, dtype=np.int)
    key_reflection = {}
    Vt = []
    First = {}
    Last = {}
    Visit = []
    priority_table = None
    result_stack = []
    raw_stack = []
    run_flag = True
    result_str = ''
    process_log = []

    construct_dict(input_grammer)
    creat_first()
    creat_last()
    create_table()
    init_find()
    analyse(input_str)
    create_str()
    return run_flag,result_str,process_log
#     print(priority_table)
#
#
#
# input_grammer="E->E+T\nE->T\nT->T*F\nT->F\nF->P^F\nF->P\nP->(E)\nP->i"
# input_grammer1="S->#E#\nE->E+T\nE->T\nT->T*F\nT->F\nF-><E>\nF->i"
# input_grammer2='E->E+E\nE->E*E\nE->(E)\nE->i'
# input_str1="T+T*F+i"
# input_str="i+i*i+i"
# operator_priority_analyse(input_grammer2,input_str)

'''
E->E+T
E->T
T->T*F
T->F
F->P^F
F->P
P->(E)
P->i
'''