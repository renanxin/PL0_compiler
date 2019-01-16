from PL0_Compiler import grammar_analyse,grammar_accuracy
import eel
import time

output_file='P_code.txt'
instructions=[]                 # 一个用来存储P_code指令集的列表，其中的每一条指令是通过一个字典存放的
stack=[]                        #运行时栈
P=None                          #指向当前运行的指令
T=None                          #指向栈顶
B=None                          #指向栈底
error_log=None                  #如果出错，则为出错信息
output_str=None                 #最后的输出结果
offset=3
run_max=1000        #最大运行次数
parament=[]
whether_wait=False
read_num=0

def load_instructions():
    global output_file,instructions
    instructions=[]
    f=open(output_file)
    content=f.readlines()
    for line in content:
        items=line.strip().split(' ')
        instructions.append({'line':int(items[0]),'A':items[1],'B':int(items[2]),'C':int(items[3])})
    f.close()

def run(whether_direct=False):
    global instructions,stack,P,T,B,error_log,output_str,offset,run_max,parament,whether_wait,read_num
    '''初始化'''
    load_instructions()
    stack = [[None, None], [None, None], [None, None]]
    P = 0
    T = -1
    B = 0
    error_log = None
    output_str = ''
    offset = 3
    run_time = 0
    run_flag = True  # 运行状态的标志
    read_num=0
    whether_wait=False
    for i in instructions:
        if i['A']=='RED':
            read_num+=1
    if read_num!=0:
        if not whether_direct:
            whether_wait=True
            eel.get_input(read_num)(creat_parament)
            while whether_wait:
                time.sleep(1)
        f=open('parament.txt')
        parament_content=f.readline()
        f.close()
        parament_content=parament_content.strip().split(' ')
        for i in parament_content[::-1]:
            parament.append(int(i))
    while run_flag:
        # for i in stack:
        #     print(i,end='  ')
        # print()
        run_time+=1
        if run_time>run_max:
            error_log='Unknown Error!'
            run_flag=False
        instruction_now=instructions[P]
        # print(instruction_now,stack,'len: ',len(stack),T,B,P)
        if instruction_now['A']=='LIT':     # 放入常数
            stack.append([int(instruction_now['C']),'const'])
            T+=1
            P+=1
        elif instruction_now['A']=='OPR':   # 执行运算
            if instruction_now['C']==0:     # 返回调用者
                if stack[B+2][0]==None:
                    run_flag=False
                    continue
                else:
                    P=stack[B+2][0]
                    T=B-1
                    B=stack[B+1][0]
                    P += 1
                    while len(stack)>T+1:
                        stack.pop()
            elif instruction_now['C']==1:       #将栈顶元素取相反数
                if T<B+offset:
                    error_log='运行时栈错误，无可用数据！'
                    run_flag = False
                elif stack[T][1]!='const':
                    error_log='无法对非数值类型变量进行运算！！'
                    run_flag = False
                else:
                    stack[T][0]=-stack[T][0]
                    P += 1
            elif instruction_now['C']==2:       #求栈顶两个元素之和
                if T<B+offset+1:
                    error_log='运行时栈错误，无可用数据！'
                    run_flag = False
                elif stack[T][1]!='const' or stack[T-1][1]!='const':
                    error_log='无法对非数值类型进行求和运算！'
                    run_flag = False
                else:
                    stack[T-1][0]=int(stack[T-1][0]+stack[T][0])
                    T-=1
                    P += 1
                    stack.pop()
            elif instruction_now['C'] ==3:      #求栈顶两个元素之差
                if T<B+offset+1:
                    error_log='运行时栈错误，无可用数据！'
                    run_flag = False
                elif stack[T][1]!='const' or stack[T-1][1]!='const':
                    error_log='无法对非数值类型进行减法运算！'
                    run_flag = False
                else:
                    stack[T-1][0]=int(stack[T-1][0]-stack[T][0])
                    T-=1
                    P += 1
                    stack.pop()
            elif instruction_now['C']==4:       #求栈顶两个元素之积
                if T<B+offset+1:
                    error_log='运行时栈错误，无可用数据！'
                    run_flag = False
                elif stack[T][1]!='const' or stack[T-1][1]!='const':
                    error_log='无法对非数值类型进行乘法运算！'
                    run_flag = False
                else:
                    stack[T-1][0]=int(stack[T-1][0]*stack[T][0])
                    T-=1
                    P += 1
                    stack.pop()
            elif instruction_now['C']==5:       #求栈顶两个元素相除
                if T<B+offset+1:
                    error_log='运行时栈错误，无可用数据！'
                    run_flag = False
                elif stack[T][1]!='const' or stack[T-1][1]!='const':
                    error_log='无法对非数值类型进行除法运算！'
                    run_flag = False
                elif stack[T][0]==0:
                    error_log = '除法分母不能为0！'
                    run_flag = False
                else:
                    stack[T-1][0]=int(stack[T-1][0]/stack[T][0])
                    T-=1
                    P += 1
                    stack.pop()
            elif instruction_now['C']==6:       #求栈顶元素模2的结果
                if T<B+offset:
                    error_log='运行时栈错误，无可用数据！'
                    run_flag = False
                elif stack[T][1]!='const':
                    error_log='无法对非数值类型进行模运算！'
                    run_flag = False
                else:
                    stack[T][0]=int(stack[T][0])%2
                    P += 1
            elif instruction_now['C'] in [8,9,10,11,12,13]:     #比较大小
                if T<B+offset+1:
                    error_log='运行时栈错误，无可用数据！'
                    run_flag = False
                elif stack[T][1]!='const' or stack[T-1][1]!='const':
                    error_log='无法对非数值类型进行比较！'
                    run_flag = False
                else:
                    if instruction_now['C']==8:
                        stack[T-1][0]=(stack[T-1][0]==stack[T][0])
                    elif instruction_now['C']==9:
                        stack[T - 1][0] = int(stack[T - 1][0] != stack[T][0])
                    elif instruction_now['C']==10:
                        stack[T - 1][0] = int(stack[T - 1][0] < stack[T][0])
                    elif instruction_now['C']==11:
                        stack[T - 1][0] = int(stack[T - 1][0] >= stack[T][0])
                    elif instruction_now['C']==12:
                        stack[T - 1][0] = int(stack[T - 1][0] > stack[T][0])
                    elif instruction_now['C']==13:
                        stack[T - 1][0] = int(stack[T - 1][0] <= stack[T][0])
                    T-=1
                    stack.pop()
                    P += 1
            elif instruction_now['C']==14:
                if T<B+offset:
                    error_log='运行时栈错误，无可用数据！'
                    run_flag = False
                elif stack[T][1]!='const':
                    error_log='无法对非数值类型进行模运算！'
                    run_flag = False
                else:
                    output_str+=str(stack[T])+' '
                    P += 1
            elif instruction_now['C']==15:
                output_str+='\n'
                P += 1
        elif instruction_now['A']=='LOD':
            B_new=B
            j=instruction_now['B']
            while j != 0:
                B_new=stack[B_new][0]
                j-=1
            load_value=B_new+instruction_now['C']
            if stack[load_value][0]==None:
                error_log="变量未赋值！"
                run_flag=False
            else:
                T+=1
                stack.append([stack[load_value][0],'const'])
                P += 1
        elif instruction_now['A']=='STO':
            B_new=B
            j=instruction_now['B']
            while j!=0:
                B_new=stack[B_new][0]
                j-=1
            input_value=B_new+instruction_now['C']
            stack[input_value][0]=stack[T][0]
            P += 1
            T-=1
            stack.pop()
        elif instruction_now['A']=='CAL':
            old_B = B
            T+=1
            B=T
            if stack[old_B][0]==None:
                stack.append([0,None])
            else:
                stack.append([stack[old_B][0],None])
            T+=1
            stack.append([old_B,None])
            T+=1
            stack.append([P,None])
            P=instruction_now['C']

            pass
        elif instruction_now['A']=='INT':
            T=B+3
            i=0
            while i<instruction_now['C']-3:
                T+=1
                stack.append([None,None])
                i+=1
            offset=instruction_now['C']
            T-=1
            P=P+1
        elif instruction_now['A']=='JMP':
            P=instruction_now['C']
        elif instruction_now['A']=='JPC':
            if T < B + offset:
                error_log = '运行时栈错误，没有可用数据！'
                run_flag = False
            if stack[T][0]==0:
                P=instruction_now['C']
            else:
                P=P+1
            T-=1
            stack.pop()
        elif instruction_now['A']=='WRT':
            if T < B + offset:
                error_log = '运行时栈错误，无可用数据！'
                run_flag = False
            elif stack[T][1] != 'const':
                error_log = '无法对非数值类型进行模运算！'
                run_flag = False
            else:
                output_str += str(stack[T][0]) + ' '
                T-=1
                stack.pop()
                P += 1
        elif instruction_now['A']=='RED':
            # value=input('请输入变量值：')
            value=parament.pop()
            B_new = B
            j = instruction_now['B']
            while j != 0:
                B_new = stack[B_new][0]
                j -= 1
            input_value = B_new + instruction_now['C']
            try:
                stack[input_value][0] = int(value)
                P += 1
            except:
                print("请正确输入！")
                run_flag=False

        else:
            error_log='未知指令！'
            run_flag=False
    if error_log!=None:
        output_str=error_log
    return output_str


# grammar_analyse('content.txt')
# if grammar_accuracy:
#     run()
#     print(output_str)
# else:
#     print('Wrong!')
def creat_parament(content):
    global whether_wait,read_num
    if content!=None:
        a=content.strip().split()
        for i in a:
            try:
                b=int(i)
            except:
                eel.show_parament_error()
                return
        if len(a)!=read_num:
            eel.show_parament_error()
            return
        f = open('parament.txt', 'w+')
        f.write(content)
        f.close()
        whether_wait=False