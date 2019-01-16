# from token_analysis import token_analyse
#
#
# symbol_table=[]     # 符号表
# layer=0             # 标记当前所属的结构层数
# layer_num={'0':3}   # 每一层中已使用的地址，每个块都空留出前三个块
# layer_dir={}        # 存放每层的父层
# state=[]            # 当前正在发生的状态列表，用来存储发生但是没有结束的命令
# now_token=None      # 当前正在处理的token
# error_list={
#     1:'应是=而不是:=',2:'=后应为数',3:'标识符后应为=',4:'const,var,procedure后应为标识符',5:'漏掉逗号或分号',6:'过程说明后的符号不正确',7:'应为语句',8:'程序体内语句部分后的符号不正确',
#     9:'应为句号',10:'语句之间漏分号',11:'标识符未说明',12:'不可向常量或过程赋值',13:'应为赋值运算符：=',14:'call后应为标识符',15:'不可调用常量或变量',16:'应为then',17:'应为分号或end',18:'应为do',
#     19:'语句后的符号不正确',20:'应为关系运算符',21:'表达式内不可有过程标识符',22:'漏右括号',23:'因子后不可为此符号',24:'表达式不能以词符号开始',30:'这个数太大',40:'应为左括号'
# }                   # 错误类型列表
# type=["关键字 ","标识符 ","常量  ","分界符 ","运算符 ","常量(小数)"]
#
# key=["const","var","procedure","odd","if","then","else","while","do","call","begin","end","repeat","until","read","write"]
#
# grammar_analyse_flag=True      # 语法分析是否正在执行
# '''
# output_file=None               # P-code代码写入的文件
# output_line_num=0              # P-code文件中当前已有的行数
# '''
# P_code=[]                      # 用来存放P-code的一个列表，同时里面的每一项都是一个命令，通过字典存储，字典的键分别为A、B和C，如果为空则为None，
#                                # 如果目前阶段不知道，则为unknown，在之后的处理过程中可以采用回填技术将其补全
# P_code_line=0
#
# procedure_addr=[]              # 一个用来存放每个过程在P_code指令中的入口的列表
#
# output_file='P_code.txt'      # 存放生成的P_code代码的文件
#
#
#
#
# def next_now_token():
#     '''
#     得到下一个token的值，如果下一个token不存在，则将grammar_analyse_flag的值置为False，停止语法分析
#     '''
#     global now_token,grammar_analyse_flag,state
#     if now_token.next!=None:
#         now_token=now_token.next
#     else:
#         grammar_analyse_flag=False
#
# def insert_variable():
#     '''
#     如果遇到了变量声明，则将变量插入符号表
#     '''
#     global now_token,symbol_table,layer_num
#     token={}
#     token['name']=now_token.name
#     token['type']='variable'
#     token['level']=int(state[-1][-1])
#     if state[-1][-1] not in layer_num.keys():
#         layer_num[state[-1][-1]]=3
#     token['addr'] = layer_num[state[-1][-1]]
#     token['deep'] = len(state)
#     layer_num[state[-1][-1]] += 1
#     symbol_table.append(token)
#
# def insert_procedure():
#     '''
#     如果遇到了过程，则将过程插入
#     '''
#     global now_token,symbol_table,layer_num
#     token={}
#     token['name']=now_token.name
#     token['type']='procedure'
#     token['level']=int(state[-1][-1])
#     if state[-1][-1] not in layer_num.keys():
#         layer_num[state[-1][-1]]=3
#     token['deep'] = len(state)
#     token['layer']=layer
#     symbol_table.append(token)
#
# def check_const():
#     '''
#     在使用一个标识符的时候使用，用来判断这个标识符是否被声明过，如果声明过，返回True，否则返回False
#     '''
#     global now_token, symbol_table, layer_dir, layer, state
#     name_now = now_token.name
#     const_value=None
#     flag = False
#     for symbol in symbol_table:  # 首先检查是否在常量中
#         if symbol['type'] == 'const':
#             if symbol['name'] == name_now:
#                 flag = True
#                 const_value=symbol['value']
#                 break
#     return flag,const_value
#
# def check_variable():
#     '''
#     在使用一个标识符的时候使用，用来判断这个标识符是否被声明过，如果声明过，返回True，否则返回False
#     '''
#     global now_token,symbol_table,layer_dir,layer,state
#     name_now=now_token.name
#     layer_now=int(state[-1][-1])
#     variable_deep=None
#     variable_addr=None
#     flag=False
#     whether_break = False       # 是否结束循环
#     while not whether_break:    # 在局部变量中寻找对应的
#         for item in symbol_table:
#             if item['type']=='variable':
#                 if item['level']==layer_now:
#                     if item['name']==name_now:      # 如果在局部变量中找到了该标识符
#                         flag=True
#                         whether_break=True
#                         variable_deep=len(state)-item['deep']
#                         variable_addr=item['addr']
#                         break
#         if layer_now in layer_dir.keys():           # 判断当前层是否有外层，如果有则将当前层设置为上一层，否则跳出循环
#             layer_now=layer_dir[layer_now]
#         else:
#             whether_break=True
#     return flag,variable_deep,variable_addr
#
# def check_procedure():
#     '''
#     在调用一个过程的时候使用，用来判断这个过程是否被声明过了，如果声明过，返回True，否则返回False
#     '''
#     global now_token, symbol_table, layer_dir, layer, state
#     name_now=now_token.name
#     layer_now=now_token.name
#     layer_now=int(state[-1][-1])
#     procedure_deep=None
#     procedure_layer=None
#     flag=False
#     whether_break=False
#     while not whether_break:
#         for item in symbol_table:
#             if item['type']=='procedure':
#                 if item['level']==layer_now:
#                     if item['name']==name_now:
#                         flag=True
#                         whether_break=True
#                         procedure_deep=len(state)-item['deep']
#                         procedure_layer=item['layer']
#                         break
#         if layer_now in layer_dir.keys():           # 判断当前层是否有外层，如果有则将当前层设置为上一层，否则跳出循环
#             layer_now=layer_dir[layer_now]
#         else:
#             whether_break=True
#     return flag,procedure_deep,procedure_layer
#
# def d_program():
#     global now_token, grammar_analyse_flag,state
#     if not  d_subprogram():
#         return False
#     if not grammar_analyse_flag or now_token.value!='.':
#         print(error_list[9])
#         return False
#     return True
#
#
# def d_subprogram():
#     global now_token,grammar_analyse_flag,state,layer,layer_dir,P_code,P_code_line,procedure_addr,layer_num
#     if len(state)!=0:
#         layer_dir[layer]=int(state[-1][-1])
#     state.append('subprogram'+str(layer))
#     layer+=1    # 已有层数加1
#     flag=True
#     instruction={}
#     instruction['line']=P_code_line
#     P_code_line+=1
#     instruction['A']='JMP'
#     instruction['B'] = 0
#     instruction['C'] = 'unknown'
#     P_code.append(instruction)
#     if now_token.type==1 and now_token.value=='const' and grammar_analyse_flag:
#         next_now_token()
#         flag=d_const_specification()
#     if flag and now_token.type==1 and now_token.value=='var' and grammar_analyse_flag:
#         next_now_token()
#         flag=d_variable_specification()
#     if flag and now_token.type == 1 and now_token.value == 'procedure' and grammar_analyse_flag:
#         next_now_token()
#         flag=d_procedure_specification()
#     if not flag:
#         return False
#     index = len(P_code) - 1
#     while index > -1:
#         if P_code[index]['C'] == 'unknown':
#             P_code[index]['C'] = P_code_line
#             break
#         index -= 1
#
#     index=len(procedure_addr)-1
#     while index>-1:
#         if procedure_addr[index][1]=='unknown':
#             procedure_addr[index][1]=P_code_line
#             break
#         index-=1
#
#     if state[-1][-1] not in layer_num.keys():
#         layer_num[state[-1][-1]]=3
#     instruction1={}
#     instruction1['line']=P_code_line
#     P_code_line+=1
#     instruction1['A']='INT'
#     instruction1['B']=0
#     instruction1['C']=layer_num[state[-1][-1]]
#     P_code.append(instruction1)
#
#     flag=d_sentence()
#     state.pop()
#     instruction={}
#     instruction['line']=P_code_line
#     P_code_line+=1
#     instruction['A']='OPR'
#     instruction['B']=0
#     instruction['C']=0
#     P_code.append(instruction)
#     return flag
#
#
# def d_const_specification():
#     global now_token,grammar_analyse_flag,state
#     flag=d_const_define()
#     if not flag:
#         return False
#     while now_token.type==4 and now_token.value==',' and grammar_analyse_flag:
#         next_now_token()
#         d_const_define()
#     if not grammar_analyse_flag:
#         print(error_list[5])
#     if now_token.type==4 and now_token.value==';' and grammar_analyse_flag:
#         next_now_token()
#         return True
#     return False
#
# def d_variable_specification():
#     global now_token,grammar_analyse_flag,state
#     if now_token.type!=2:
#         print(error_list[4])
#         return False
#     insert_variable()
#     next_now_token()
#     flag=True
#     while flag and now_token.value==',' and  grammar_analyse_flag:
#         next_now_token()
#         if not grammar_analyse_flag or now_token.type!=2:
#                 flag=False
#                 continue
#         if flag and grammar_analyse_flag:
#             insert_variable()
#         next_now_token()
#     if flag==False:
#         print(error_list[4])
#         return False
#     if not grammar_analyse_flag or now_token.value!=';':
#         print(error_list[5])
#         return False
#     next_now_token()
#     return True
#
# def d_procedure_specification():
#     global now_token,grammar_analyse_flag,procedure_addr,layer
#     if not grammar_analyse_flag or now_token.type!=2:
#         print(error_list[4])
#         return False
#     if check_procedure()[0]:
#         print('过程名重复！')
#         return False
#     insert_procedure()
#     procedure_addr.append([now_token.name,'unknown',layer])
#     next_now_token()
#     if not grammar_analyse_flag or now_token.value!=';':
#         print(error_list[5])
#         return False
#     next_now_token()
#     if not d_subprogram():
#         return False
#     if not grammar_analyse_flag or now_token.value!=';':
#         print(error_list[5])
#         return False
#     next_now_token()
#     if not grammar_analyse_flag or now_token.value!='procedure':
#         return True
#     next_now_token()
#     return d_procedure_specification()
#
# def d_sentence():
#     global now_token,grammar_analyse_flag,P_code,P_code_line
#     if now_token.type==2:
#         return d_assign_sentence()
#     if now_token.value=='if':
#         return d_condition_sentence()
#     if now_token.value=='while':
#         return d_loop_sentence()
#     if now_token.value=='call':
#         return d_procedure_call_sentence()
#     if now_token.value=='read':
#         return d_read_sentence()
#     if now_token.value=='write':
#         return d_write_sentence()
#     if now_token.value=='begin':
#         return d_complex_sentence()
#     if now_token.value=='repeat':
#         return d_repeat_sentence()
#     return True
#
# def d_const_define():
#     global now_token,grammar_analyse_flag,state
#     if now_token.type==2:
#         if check_const()[0]:
#             print('该常量重复声明！')
#         token={}
#         token['name']=now_token.name
#         token['type']='const'
#         next_now_token()
#         if not grammar_analyse_flag or now_token.value!='=':
#             print(error_list[3])
#             return False
#         next_now_token()
#         if not grammar_analyse_flag or now_token.type!=3:
#             print(error_list[2])
#             return False
#         token['value']=int(now_token.value)
#         symbol_table.append(token)
#         next_now_token()
#         return True
#     else:
#         print(error_list[4])
#         return False
#
# def d_assign_sentence():
#     global now_token, grammar_analyse_flag,P_code_line,P_code
#     if not check_variable()[0] and (check_const() or check_procedure()[0]):
#         print(error_list[12])
#         return False
#     if not  check_variable()[0]:
#         print(error_list[11])
#         return False
#
#     instruction = {}
#     flag,variable_deep,variable_addr=check_variable()
#     instruction['A']='STO'
#     instruction['B']=variable_deep
#     instruction['C']=variable_addr
#
#     next_now_token()
#     if not grammar_analyse_flag or now_token.value != ':=':
#         print(now_token.value)
#         print(error_list[13])
#         return False
#     next_now_token()
#     if not grammar_analyse_flag:
#         print('缺少表达式！')
#     result=d_expression()
#     instruction['line'] = P_code_line
#     P_code_line += 1
#     P_code.append(instruction)
#     return result
#
# def d_condition_sentence():
#     global now_token, grammar_analyse_flag,P_code,P_code_line
#     next_now_token()
#     if not grammar_analyse_flag:
#         print("条件！")
#         return False
#     if not d_condition():
#         return False
#     if now_token.value != 'then':
#         print(error_list[16])
#         return False
#     next_now_token()
#     if not d_sentence():
#         return False
#     index = len(P_code) - 1
#     while index > -1:
#         if P_code[index]['C'] == 'unknown':
#             P_code[index]['C'] = P_code_line
#             break
#         index -= 1
#     if not grammar_analyse_flag or now_token.value != 'else':
#         return True
#     next_now_token()
#     if not d_sentence():
#         return False
#     return True
#
# def d_loop_sentence():
#     global now_token,grammar_analyse_flag,P_code,P_code_line
#     next_now_token()
#     if not grammar_analyse_flag:
#         print('缺少条件！')
#         return False
#     addr_back = P_code_line
#     if not d_condition():
#         return False
#     if not grammar_analyse_flag:
#         print(error_list[18])
#         return False
#     next_now_token()
#     if not d_sentence():
#         return False
#     instruction={}
#     instruction['line']=P_code_line
#     P_code_line+=1
#     instruction['A']='JMP'
#     instruction['B']=0
#     instruction['C']=addr_back
#     P_code.append(instruction)
#     index=len(P_code)-1
#     while index>-1:
#         if P_code[index]['C']=='unknown':
#             P_code[index]['C']=P_code_line
#             break
#         index-=1
#     return True
#
# def d_procedure_call_sentence():
#     global now_token, grammar_analyse_flag,P_code,P_code_line,procedure_addr
#     next_now_token()
#     if check_variable()[0] or check_const()[0]:
#         print(error_list[15])
#         return False
#     if not check_const()[0] and not check_variable()[0] and not check_procedure()[0]:
#         print(error_list[11])
#         return False
#     if not grammar_analyse_flag or now_token.type!=2:
#         print(error_list[14])
#         return False
#     instruction={}
#     instruction['line']=P_code_line
#     P_code_line+=1
#     instruction['A']='CAL'
#     flag,procedure_deep,procedure_layer=check_procedure()
#     instruction['B']=procedure_deep
#     addr=None
#     for i in procedure_addr:
#         if i[0]==now_token.name and i[2]==procedure_layer:
#             addr=i[1]
#     instruction['C']=addr
#     P_code.append(instruction)
#     next_now_token()
#     return True
#
# def d_read_sentence():
#     global now_token, grammar_analyse_flag,P_code,P_code_line
#     next_now_token()
#     if not grammar_analyse_flag or now_token.value!='(':
#         print(error_list[40])
#         return False
#     next_now_token()
#     if not grammar_analyse_flag or now_token.type!=2:
#         print('应为标识符！')
#         return False
#     if not check_variable()[0]:
#         print(error_list[11])
#         return False
#
#     instruction={}
#     instruction['line']=P_code_line
#     P_code_line+=1
#     flag,variable_deep,variable_addr=check_variable()
#     instruction['A']='RED'
#     instruction['B']=variable_deep
#     instruction['C']=variable_addr
#     P_code.append(instruction)
#
#     next_now_token()
#     flag_loop=False
#     while grammar_analyse_flag and now_token.value==',':
#         flag_loop=True
#         next_now_token()
#         if not grammar_analyse_flag or now_token.type!=2:
#             print('应为标识符！')
#             return False
#         if not check_variable()[0]:
#             print(error_list[11])
#             return False
#
#         instruction = {}
#         instruction['line'] = P_code_line
#         P_code_line += 1
#         flag, variable_deep, variable_addr = check_variable()
#         instruction['A'] = 'RED'
#         instruction['B'] = variable_deep
#         instruction['C'] = variable_addr
#         P_code.append(instruction)
#
#     if flag_loop:
#         next_now_token()
#     if not grammar_analyse_flag or now_token.value!=')':
#         print(error_list[22])
#         return False
#     next_now_token()
#     return True
#
# def d_write_sentence():
#     global now_token, grammar_analyse_flag,P_code,P_code_line
#     next_now_token()
#     if not grammar_analyse_flag or now_token.value != '(':
#         print(error_list[40])
#         return False
#     next_now_token()
#     if not d_expression():
#         return False
#     instruction={'line':P_code_line,'A':'WRT','B':0,'C':0}
#     P_code_line+=1
#     P_code.append(instruction)
#     while grammar_analyse_flag and now_token.value == ',':
#         next_now_token()
#         if not d_expression():
#             return False
#         instruction = {'line': P_code_line, 'A': 'WRT', 'B': 0, 'C': 0}
#         P_code_line += 1
#         P_code.append(instruction)
#     if not grammar_analyse_flag or now_token.value != ')':
#         print(error_list[22])
#         return False
#     instruction = {'line': P_code_line, 'A': 'OPR', 'B': 0, 'C': 15}
#     P_code_line += 1
#     P_code.append(instruction)
#     next_now_token()
#     return True
#
# def d_complex_sentence():
#     global now_token, grammar_analyse_flag
#     next_now_token()
#     if not d_sentence():
#         return False
#     while grammar_analyse_flag and now_token.value==';':
#         next_now_token()
#         if not d_sentence():
#             return False
#     if not grammar_analyse_flag or now_token.value!='end':
#         print(now_token.value)
#         print(error_list[17])
#         return False
#     next_now_token()
#     return True
#
# def d_repeat_sentence():
#     global now_token, grammar_analyse_flag,P_code,P_code_line
#     next_now_token()
#     addr_back=P_code_line
#     if not d_sentence():
#         return False
#     while grammar_analyse_flag and now_token.value==';':
#         next_now_token()
#         if not d_sentence():
#             return False
#     if not grammar_analyse_flag or now_token.value!='until':
#         print('应为until ！')
#         return False
#     next_now_token()
#     if not grammar_analyse_flag:
#         print('应为条件！')
#         return False
#     if not d_condition():
#         return False
#     index = len(P_code)-1
#     while index > -1:
#         if P_code[index]['C']=='unknown':
#             P_code[index]['C']=addr_back
#             break
#         index-=1
#     return True
#
# def d_expression():
#     global now_token, grammar_analyse_flag,P_code_line,P_code
#     is_negative=False
#     if now_token.value=='+' or now_token.value=='-':
#         if now_token.value=='-':
#             is_negative=True
#         next_now_token()
#     if not grammar_analyse_flag:
#         print('缺少项！！')
#         return False
#     if not d_term():
#         return False
#     if not grammar_analyse_flag:
#         return True
#     flag=True
#     if is_negative:
#         instruction={}
#         instruction['line'] = P_code_line
#         P_code_line += 1
#         instruction['A'] = 'OPR'
#         instruction['B'] = 0
#         instruction['C'] = 1
#         P_code.append(instruction)
#     operate={'+':2,'-':3}
#     while grammar_analyse_flag and flag and (now_token.value=='+' or now_token.value=='-'):
#         instruction = {}
#         instruction['A'] = 'OPR'
#         instruction['B'] = 0
#         instruction['C'] = operate[now_token.value]
#         next_now_token()
#         if not grammar_analyse_flag:
#             print('缺少项！')
#             return False
#         if not d_term():
#             flag=False
#         instruction['line'] = P_code_line
#         P_code_line += 1
#         P_code.append(instruction)
#     if not flag:
#         return False
#     return True
#
# def d_term():
#     global now_token, grammar_analyse_flag,P_code,P_code_line
#     if not d_factor():
#         return False
#     if not grammar_analyse_flag:
#         return True
#     flag=True
#     operate={'*':4,'/':5}
#     while grammar_analyse_flag and flag and (now_token.value=='*' or now_token.value=='/'):
#         instruction={}
#         instruction['A'] = 'OPR'
#         instruction['B'] = 0
#         instruction['C'] = operate[now_token.value]
#         flag_loop=True
#         next_now_token()
#         if not grammar_analyse_flag:
#             print('缺少因子！')
#             return False
#         if not d_factor():
#             flag=False
#         instruction['line'] = P_code_line
#         P_code_line += 1
#         P_code.append(instruction)
#     if not flag:
#         return False
#     return True
#
# def d_factor():
#     global now_token, grammar_analyse_flag,P_code,P_code_line
#     if now_token.type==2:
#         if check_procedure()[0]:
#             print('过程不可以作为因子！')
#             return False
#         if not check_variable()[0] and not check_const()[0]:
#             print(error_list[11])
#             return False
#     if now_token.type==2 or now_token.type==3:
#         instruction={}
#         instruction['line']=P_code_line
#         P_code_line+=1
#         if now_token.type==2:
#             if check_variable()[0]:
#                 instruction['A'] = 'LOD'
#                 flag,variable_deep,variable_addr=check_variable()
#                 instruction['B']=variable_deep
#                 instruction['C']=variable_addr
#             else:
#                 instruction['A'] = 'LIT'
#                 flag,variable_value = check_const()
#                 instruction['B'] = 0
#                 instruction['C'] = variable_value
#             P_code.append(instruction)
#         if now_token.type==3:
#             instruction['A'] = 'LIT'
#             instruction['B'] = 0
#             instruction['C'] = now_token.value
#             P_code.append(instruction)
#         next_now_token()
#         return True
#     if not now_token.value=='(':
#         print('缺少因子')
#         return False
#     next_now_token()
#     if not grammar_analyse_flag:
#         print('缺少表达式！')
#         return False
#     if not d_expression():
#         return False
#     if not grammar_analyse_flag or now_token.value!=')':
#         print(error_list[22])
#         return False
#     next_now_token()
#     return True
#
# def d_condition():
#     global now_token,grammar_analyse_flag,P_code,P_code_line
#     if now_token.value=='odd':
#         next_now_token()
#         if not grammar_analyse_flag:
#             print('缺少表达式！')
#             return False
#         if not d_expression():
#             return False
#         instruction={}
#         instruction1={}
#         instruction['line']=P_code_line
#         P_code_line+=1
#         instruction['A']='OPR'
#         instruction['B']=0
#         instruction['C']=6
#         P_code.append(instruction)
#
#         instruction1['line'] = P_code_line
#         P_code_line += 1
#         instruction1['A'] = 'JPC'
#         instruction1['B'] = 0
#         instruction1['C'] = 'unknown'
#         P_code.append(instruction1)
#         return True
#     if not d_expression():
#         return False
#     operate_mapping={'=':8,'<>':9,'<':10,'>=':11,'>':12,'<=':13}
#     if now_token.value not in ['=','<>','<','<=','>','>=']:
#         print(error_list[20])
#         return False
#     operate_now=now_token.value
#     next_now_token()
#     if not grammar_analyse_flag:
#         print('缺少表达式！')
#         return False
#     if not d_expression():
#         return False
#     instruction={}
#     instruction1={}
#     instruction['line'] = P_code_line
#     P_code_line += 1
#     instruction['A'] = 'OPR'
#     instruction['B'] = 0
#     instruction['C'] = operate_mapping[operate_now]
#     P_code.append(instruction)
#
#     instruction1['line']=P_code_line
#     P_code_line+=1
#     instruction1['A']='JPC'
#     instruction1['B']=0
#     instruction1['C']='unknown'
#     P_code.append(instruction1)
#     return True
#
# def creat_outputfile():
#     global output_file,P_code
#     f=open(output_file,'w+')
#     instruction=''
#     for i in P_code:
#         instruction += str(i['line']) + ' '
#         instruction += i['A'] + ' '
#         instruction += str(i['B']) + ' '
#         instruction += str(i['C'])
#         instruction += '\n'
#     f.write(instruction[:-1])
#     f.close()
#
# def grammar_analyse(file):
#     '''
#     语法分析程序
#     :param text:前端传来的文件中的内容
#     :return:
#     '''
#     global now_token,output_file
#     flag, token_head, log=token_analyse(file)
#     now_token=token_head.next
#     flag=d_program()
#     creat_outputfile()
#     return flag
#
#
# file='content.txt'
# grammar_analyse(file)