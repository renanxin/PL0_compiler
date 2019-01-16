# # -*- coding: utf-8 -*-
# from tkinter import *
# from tkinter.filedialog import askopenfilename
# import tkinter.messagebox
# import os
# from token_analysis import token_analyse,type
# from tkinter import ttk
#
#
# def center_window(root, width, height):
#     screenwidth = root.winfo_screenwidth()
#     screenheight = root.winfo_screenheight()
#     size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
#     root.geometry(size)
#
#
# def selectPath():
#     path_ = askopenfilename()
#     path.set(path_)
#
# def rewrite():
#     if not os.path.exists(path.get()):
#         tkinter.messagebox.showinfo('警告', '请确定文件路径正确！')
#         return
#     try:
#         v1 = StringVar()
#         f=open(path.get())
#         content=f.readlines()
#         for line in content:
#             v1.set(v1.get()+line)
#         f.close()
#         top = Toplevel()
#         top.title("文件修改")
#         text1 = Text(top,bg='#DCDCDC')
#         text1.grid(row=0,sticky=N+S+W)
#         bar=Scrollbar(top)
#         bar.grid(row=0,sticky=N+S+E)
#         bar.config(command=text1.yview)
#         text1.config(yscrollcommand=bar.set)
#         text1.insert(END,v1.get())
#         fr1=LabelFrame(top)
#         fr1.grid(row=1,column=0,columnspan=2,sticky=E+W)
#
#         def key_Cancel():
#             top.destroy()
#
#         def key_Save():
#             content_now=text1.get('0.0',END)
#             content_now=content_now[:-1]
#             f=open(path.get(),'w+')
#             f.write(content_now)
#             f.close()
#             top.destroy()
#             tkinter.messagebox.showinfo('提示', '修改文件成功！')
#
#         b1=Button(fr1,text=' Save ',command=key_Save)
#         b1.pack(padx=10,side=RIGHT)
#         b2=Button(fr1,text='Cancel',command=key_Cancel)
#         b2.pack(padx=10,side=RIGHT)
#     except:
#         tkinter.messagebox.showinfo('警告', '文件格式不对！')
#
#
#
# def compile_Start():
#     if not os.path.exists(path.get()):
#         tkinter.messagebox.showinfo('警告', '请确定文件路径正确！')
#         return
#     try:
#         top=Toplevel()
#         top.title('运行结果')
#         flag,log_now=token_analyse(path.get())
#         if flag:
#             fr3=LabelFrame(top)
#             fr3.grid(row=0,column=0,columnspan=4)
#             text_result=ttk.Treeview(fr3,columns=('c1','c2','c3'),show='headings')
#             text_result.grid(row=0,sticky=N+S+W)
#             bar=Scrollbar(fr3)
#             bar.grid(row=0,sticky=N+S+E)
#             bar.config(command=text_result.yview)
#             text_result.config(yscrollcommand=bar.set)
#             text_result.heading('c1',text='单词')
#             text_result.heading('c2',text='类别')
#             text_result.heading('c3',text='值')
#             t=log_now.next
#             i=0
#             while(t != None):
#                 if t.type==3:
#                     text_result.insert('',i,values=[t.name,type[t.type - 1],str(bin(int(t.value)))+'<二进制>'])
#                 else:
#                     text_result.insert('', i, values=[t.name, type[t.type - 1], t.value])
#                 t=t.next
#                 i+=1
#         else:
#             fr3=LabelFrame(top,height=100)
#             fr3.grid(row=0,column=0,columnspan=4)
#             text_result = Text(fr3,bg='SkyBlue')
#             text_result.grid(row=0,sticky=N+W)
#             bar=Scrollbar(fr3)
#             bar.grid(row=0,sticky=N+S+E)
#             bar.config(command=text_result.yview)
#             text_result.config(yscrollcommand=bar.set)
#             text_result.config(state=NORMAL)
#             text_result.delete('1.0','end')
#             text_result.insert(END,log_now)
#             text_result.config(state=DISABLED)
#     except:
#         tkinter.messagebox.showinfo('警告', '文件格式不对！')
#
# def change_content():
#     try:
#         selectPath()
#         v1 = StringVar()
#         f = open(path.get())
#         content = f.readlines()
#         for line in content:
#             v1.set(v1.get() + line)
#         f.close()
#         text.config(state=NORMAL)
#         text.delete('1.0', 'end')
#         text.insert(END, v1.get())
#         text.config(state=DISABLED)
#     except:
#         text.config(state=NORMAL)
#         text.delete('1.0', 'end')
#         text.insert(END, '无法预览文件，请检查文件路径或文件格式！')
#         text.config(state=DISABLED)
#
# root = Tk()
# root.title("PL0编译器")
#
# path = StringVar()
#
# Label(root,text = "目标文件:").grid(row = 0, column=0)
# Entry(root, textvariable = path,bg='Azure').grid(row = 0,column=1)
# Button(root, text = "路径选择", bg='Blue',command = change_content).grid(row = 0,column=2)
# Button(root, text = "修改文件", bg='Blue',command = rewrite).grid(row = 0,column=3)
# Button(root, text = "开始编译", command = compile_Start,bg="gray").grid(row = 1,column=0)
#
# fr2=LabelFrame(root)
# fr2.grid(row=2,column=0,columnspan=4)
# text = Text(fr2,bg='#DCDCDC')
# text.grid(row=0,sticky=N+S+W)
# bar=Scrollbar(fr2)
# bar.grid(row=0,sticky=N+S+E)
# bar.config(command=text.yview)
# text.config(yscrollcommand=bar.set)
# text.config(state=DISABLED)
#
# root.mainloop()

import eel
from token_analysis import token_analyse,type
from operator_priority_analyzer import operator_priority_analyse



# @eel.expose
# def your_python_function(a):
#     file_name='content.txt'
#     f=open(file_name,'w+')
#     f.write(a)
#     f.close()
#     flag,log,error_log=token_analyse(file_name)
#     result='name        type        value        \n'
#     while(log.next!=None):
#         log=log.next
#         if log.type==3:
#             text=log.name+' '*(13-len(log.name+'1'))+type[log.type-1]+' '*(13-len(type[log.type-1]+'1'))+str(bin(int(log.value)))+'<二进制>'+' '*(13-len(str(bin(int(log.value)))+'<二进制>'+'1'))
#         else:
#              text = log.name + ' ' * (13 - len(log.name + '1')) + type[log.type - 1] + ' ' * (
#                             13 - len(type[log.type - 1] + '1')) + log.value + ' ' * (
#                                    13 - len(log.value+'1'))
#         result=result+text+'\n'
#     log=result
#     if not flag:
#         log+=log+'\n\n\n'+error_log
#     eel.show_return(flag,log)
# eel.init('')
# eel.start('main_interface.html')



# @eel.expose
# def your_python_function(grammar,code):
#     run_flag, result_str, process_log=operator_priority_analyse(grammar,code)
#     str_=''
#     str_=str_+'Step'.ljust(6,' ')+'Stack'.ljust(10,' ')+'Priority'.ljust(10,' ')+'Char'.ljust(8,' ')+'rest'.ljust(10,' ')+'Action'.ljust(10,' ')+'\n'
#     for i in range(len(process_log)):
#         str_=str_+str(i+1).ljust(6,' ')+process_log[i][0].ljust(10,' ')+process_log[i][1].ljust(10,' ')+process_log[i][2].ljust(8,' ')+process_log[i][3].ljust(10,' ')+process_log[i][4].ljust(10,' ')+'\n'
#     process_log=str_[:-1]
#     eel.show_return(run_flag,result_str,process_log)
#
#
# eel.init('')
#
#
# eel.start('operator_priority_interface.html')

from PL0_Compiler import grammar_analyse
from run import run
compile_flag=False
run_flag=False

@eel.expose
def compile(content,type,run_flag):
    global compile_flag
    file = 'content.txt'
    if type==0:
        f=open(file,'w+')
        f.write(content)
        f.close()
        grammar_accuracy, symbol_table, error_information,token_flag,token_log=grammar_analyse(file)
        if token_flag:
            if grammar_accuracy:compile_flag=True
            else:compile_flag=False
            eel.show_compiler_result(grammar_accuracy)
        else:
            compile_flag=False
            eel.show_compiler_result(token_log)


    elif type==1:
        grammar_accuracy, symbol_table, error_information,token_flag,token_log = grammar_analyse(file)
        i=len(str(len(symbol_table)))
        log=' '.rjust(i,' ')+'   '+'name'.ljust(8,' ')+'type'.ljust(10,' ')+'value'.ljust(8,' ')+'addr'.ljust(6,' ')+'deep'.ljust(8,' ')+'level'.ljust(8,' ')+'\n'
        for j in range(len(symbol_table)):
            if symbol_table[j]['type']=='const':
                item_log=str('%d'%(j+1)).rjust(i,' ')+'   '+str(symbol_table[j]['name']).ljust(8,' ')+'CONST'.ljust(10,' ')+str(symbol_table[j]['value']).ljust(8,' ')+''.ljust(6,' ')+''.ljust(8,' ')+''.ljust(8,' ')+'\n'
            elif symbol_table[j]['type']=='variable':
                item_log = str('%d' % (j + 1)).rjust(i, ' ') + '   ' + str(symbol_table[j]['name']).ljust(8,' ') + 'VARIABLE'.ljust(10, ' ') + ''.ljust(8, ' ') + str(symbol_table[j]['addr']).ljust(6, ' ') + str(symbol_table[j]['deep']).ljust(8, ' ') + str(symbol_table[j]['level']).ljust(8,' ') + '\n'
            elif symbol_table[j]['type']=='procedure':
                item_log = ('%d' % (j + 1)).rjust(i, ' ') + '   ' + str(symbol_table[j]['name']).ljust(8,' ') + 'PROCEDURE'.ljust(10, ' ') + ''.ljust(8, ' ') + ''.ljust(6, ' ') + str(symbol_table[j]['deep']).ljust(8, ' ') + str(symbol_table[j]['level']).ljust(8,' ') + '\n'
            log+=item_log
        eel.show_symbol(log[:-1])
    elif type==2:
        grammar_accuracy, symbol_table, error_information ,token_flag,token_log= grammar_analyse(file)
        if token_flag:
            if error_information==[]:
                error_log='There is no mistake here.'
            else:
                error_log=''
                for i in range(len(error_information)):
                    log='%d. '%(i+1)+error_information[i]+'\n'
                    error_log+=log
                error_log=error_log[:-1]
            eel.show_error_log(error_log)
        else:
            eel.show_error_log(token_log)
    elif type==3:
        f=open('P_code.txt')
        lines=f.readlines()
        num=len(lines[-1].split(' ')[0])
        log=''
        for line in lines:
            a,b,c,d=line.split(' ')
            a=a.rjust(num,' ')
            b=b.rjust(5,' ')
            c=c.rjust(6,' ')
            d=d.ljust(7,' ')
            e=('      ')
            log=log+a+b+c+e+d+'\n'
        eel.show_P_code(log)
    elif type==4:
        if compile_flag==True and run_flag==True:
            output=run(whether_direct=True)
        elif not compile_flag:
            output='请先编译成功！'
        elif not run_flag:
            output = '请先运行成功！'
        eel.show_run_result(output)
    elif type==5:
        if compile_flag==True:
            output=run(whether_direct=False)
        else:
            output = '请先编译成功！'
        eel.show_run_result(output)



eel.init('')
eel.start('Compiler.html')