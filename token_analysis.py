import numpy as np

class Sentence:
    def __init__(self,value):
        self.data=value
        self.next=None

class Token:
    def __init__(self,name,type,value):
        self.name=name
        self.type=type
        self.value=value
        self.next=None
        self.line=0
        self.position=0

sentence_head=Sentence(None)
sentence_p=Sentence(None)
token_head=Token(None,None,None)
token_p=Token(None,None,None)

flag=True
isend=False
iscomment=False

ch=''
key=["const","var","procedure","odd","if","then","else","while","do","call","begin","end","repeat","until","read","write"]
token=np.array(['\0']*255)
word=''
type=["关键字 ","标识符 ","常量  ","分界符 ","运算符 ","常量(小数)"]

log=''
error_log=''

line_now=1          #当前单词所在的行数
position=1          #当前单词在行中的位置


def remove_comments():
    global iscomment,ch,isend
    while not isend:
        get_Char()
        if ch=='*':
            if isend:
                return
            get_Char()
            if ch=='/':
                iscomment=False
                return
            retract()
    return

def get_Char():
    global sentence_p,ch,isend
    sentence_p=sentence_p.next
    if(sentence_p==None):
        isend=True
        return
    ch=sentence_p.data

def get_nbc():
    while(ch==' ' or ch=='\t'or ch=='\n'):
        if isend:
            return
        get_Char()

def cat():
    global token,ch
    len=np.sum(token!='\0')
    token[len]=ch
    token[len+1]='\0'

def isletter(ch):
    return ch.isalpha()

def isdigit(ch):
    return ch.isdigit()

def retract():
    global sentence_head,sentence_p
    l=sentence_head
    while(l.next!=sentence_p):
        l=l.next
    sentence_p=l

def isreserve():
    global word,key
    key_judge=0
    for key_judge in range(16):
        if word==key[key_judge]:
            return key_judge
        key_judge+=1
    return -1

def error(num,file):
    global flag,log,error_log
    flag = False
    # log = log + "错误信息如下:\n"
    # error_log = error_log + "========================================\n"
    error_log = error_log +('Error: The %s in the line %d is not correct!\n'%(ch,num))
    # error_log = error_log + "========================================"

def scanner(num,file):
    '''
    扫描字符
    :param num: 当前处理的行数
    :param file: 处理文件路径
    '''
    global token_p,token_head,sentence_p,sentence_head,isend,iscomment,word,line_now,position
    c=0
    j=0
    for j in range(255):
        token[j]='\0'
    if isend:
        return
    get_Char()
    if isend:
        return
    get_nbc()
    if isend:
        return
    error_happen=False
    if(ch>='a' and ch<='z' or ch>='A' and ch<='Z'):
        while(ch>='a' and ch<='z' or ch>='A' and ch<='Z' or isdigit(ch)):
            cat()
            get_Char()
            if isend:
                break
        if not isend:
            retract()
        len=np.sum(token!='\0')
        word=''.join(token[:len])
        c=isreserve()
        t=Token(word,None,None)
        if(c==-1):
            t.type=2
            t.value=word
            t.line=line_now
            t.position=position
            token_p.next=t
            token_p=t
        else:
            t.type=1
            t.value=key[c]
            t.line = line_now
            t.position = position
            token_p.next=t
            token_p=t
    elif isdigit(ch):
        isdecimal=False
        while(isdigit(ch)):
            cat()
            get_Char()
            if isend:
                break
        if ch=='.':
            isdecimal=True
            cat()
            get_Char()
            while(isdigit(ch)):
                cat()
                get_Char()
                if isend:
                    break
        if not isend:
            retract()
        len = np.sum(token != '\0')
        word = ''.join(token[:len])
        type=6 if isdecimal else 3
        t=Token(word,type,word)
        t.line = line_now
        t.position = position
        token_p.next=t
        token_p=t
    elif ch=='/':
        get_Char()
        if isend:
            t=Token('/',5,'/')
            t.line = line_now
            t.position = position
            token_p.next=t
            token_p=t
        elif ch=='/':
            isend=True
            return
        elif ch=='*':
            iscomment=True
            return
        else:
            retract()
            t = Token('/', 5, '/')
            t.line = line_now
            t.position = position
            token_p.next = t
            token_p = t
    else:
        name=''
        type=''
        value=''
        t=Token(None,None,None)
        if ch=='+' or ch=='-' or ch=='*' :
            name=ch
            type=5
            value=ch
        elif ch==':':
            get_Char()
            if ch=='=':
                name=':='
                type=5
                value=':='
            else:
                error(num,file)
        elif ch=='=':
            name='='
            type=5
            value='='
        elif ch=='<':
            get_Char()
            if ch=='=':
                name='<='
                type=5
                value='<='
            elif ch=='>':
                name='<>'
                type=5
                value='<>'
            else:
                retract()
                name='<'
                type=5
                value='<'
        elif ch=='>':
            get_Char()
            if ch=='=':
                name='>='
                type=5
                value='>='
            else:
                name='>'
                type=5
                value='>'
                retract()
        elif ch==',' or ch==';' or ch=='(' or ch==')' or ch=='.':
            name=ch
            type=4
            value=ch
        else:
            error(num,file)
            error_happen=True
        if not error_happen:
            t = Token(name, type, value)
            t.line = line_now
            t.position = position
            token_p.next = t
            token_p = t
    position+=1

def push_sentence(s):
    global sentence_p,sentence_head
    len=s.__len__()
    sentence_p=sentence_head
    sentence_p.next=None
    for i in range(len):
        sen=Sentence(s[i])
        sentence_p.next=sen
        sentence_p=sentence_p.next
    sentence_p=sentence_head


def token_analyse(file):
    global token_p,token_head,sentence_p,sentence_head,isend,log,flag,iscomment,error_log,line_now,position
    line_now=1
    position=1
    flag=True
    log=''
    error_log=''
    f=open(file)
    num=1
    token_p=token_head
    token_p.next=None
    line=f.readline()
    while(line):
        push_sentence(line.strip())
        isend=False
        if iscomment:
            remove_comments()
        while(sentence_p!=None):
            if isend:
                break
            if iscomment:
                remove_comments()
            scanner(num,file)
        num+=1
        line=f.readline()
        line_now+=1
        position=1
    if flag:
        return flag,token_head,''
    log = log + "错误信息如下:\n"
    log = log + "========================================\n"
    log = log + error_log
    log = log + "========================================"
    return flag,token_head,log

# print(token_analyse('content.txt')[2])