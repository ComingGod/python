###-*- coding: cp936 -*-
##x=1
##y=2
##z=x+y
##print(z)
##if z>=3:
##     print("¾Í¹þ¹þ")

####################################Ñ­»·#####################
########  {0}{1}{2}´ú±í.formatÀïÃæµÄÄÚÈÝ¡£formatÓÃÀ´Á¬½Ó
########
############for i in range(0,3):
############    print(i)
############    # print("Index"+i)
############    print("Index {0} {2} {1}".format(i,"cnblogs","test"))
############print("end")
############
############

#################################   º¯Êý   ##################
##########def HelloCNBlogs():
##########    print("Hello cnblogs")
##########
##########def GetMax(x,y):
##########    if x>y:
##########        return x
##########    else:
##########        return y
##########HelloCNBlogs()
##########print(GetMax(9,3))



#################################   Àà   ##################
########## selfÀàËÆthisÖ¸Õë
########## _init_ÊÇÀàµÄ¹¹Ôìº¯Êý
##########  sayfirstÎªÊµÀý»¯firsttset£¬ÒòÎªfirsttestµÄ¹¹Ôìº¯ÊýÓÐ¸ö²ÎÊý£¬ËùÒÔÔÚÊµÀý»¯µÄÊ±ºò±ØÐë´«ÈëÒ»¸ö²ÎÊý
########class FirstTest:
########    def __init__(self,name):
########        self._name=name
########    def SayFirst(self):
########        print("Hello {0}".format(self._name))
########F = FirstTest("CNBlogs")
########F.SayFirst()


#################################   ¼Ì³Ð   ##################
#########×ÓÀà£¨¸¸Àà£© ÆäËûÓïÑÔÊÇ×ÓÀà£º¸¸Àà

##class FirstTest:
##    def __init__(self,name):
##        self._name=name
##    def SayFirst(self):
##        print("Hello {0}".format(self._name))
##
##class SecondTest(FirstTest):
##    def __init__(self,name):
##        FirstTest.__init__(self,name)
##    def SaySecond(self):
##        print("Good {0}".format(self._name))
        
##S=SecondTest("CNBlogs");
##S.SayFirst()
##S.SaySecond();


#########################        ÒýÓÃÆäËûÎÄ¼þÖÐµÄÀà      ##############
######
######### µÚÒ»ÖÖÒýÈëµÄ·½·¨
######### import FirstWork
#########
######### S=FirstWork.SecondTest("CNBlogs");
######### S.SayFirst()
######### S.SaySecond();
########
#########µÚ¶þÖÖÒýÈë·½·¨
########
########from FirstWork import SecondTest
########
########ST=SecondTest("CNBlogs");
########ST.SayFirst()
########ST.SaySecond();


#########################        µ¥ÒýºÅË«ÒýºÅÈýÒýºÅµÄÊ¹ÓÃ      ##############
######ÈýÒýºÅ¿ÉÒÔ»»ÐÐÊ¹ÓÃ
####dan='m1n9'
####print("dan:  {0}".format(dan))
####dan1='Our "young"!'
####print("dan1:  {0}".format(dan1))
####dan2='''Our
####young
####cool'''
####print("dan2:  {0}".format(dan2))
####dan3="""Our
####young
####cool"""
####print("dan3:  {0}".format(dan3))



#########################        ×ªÒå×Ö·û¸ú»»ÐÐ·ûµÄÊ¹ÓÃ      ##############
####
##
##comment='I\'m young'
##print(comment)
##description="Our \nyoung"
##print(description)
##


#########################       ×ÔÈ»×Ö·û¸úÖØ¸´×Ö·ûµÄÊ¹ÓÃ      ##############
##×ÔÈ»×Ö·û´®×ÖÃæÒâË¼Àí½â¾ÍÊÇ½«×Ö·û´®±£Áô±¾ÉíµÄ¸ñÊ½£¬¶ø²»ÊÜ×ªÒåµÄÓ°Ïì¡£
##×Ö·û´®ÖØ¸´×ÖÃæÒâË¼Àí½â¾ÍÊÇ½«×Ö·û´®ÖØ¸´Êä³ö¡£
##comment=r'Our \nyoung'
##print(comment)
##description="Our \nyoung"
##print(description)
##
##three="Our young\n"*3
##print(three)



#########################       ×Ó×Ö·û´®     ##############
##Ë÷ÒýÔËËã·û´Ó0¿ªÊ¼Ë÷Òý
#ÇÐÆ¬ÔËËã·û[x:y]ÊÇÖ¸´ÓµÚxÏÂ±ê¿ªÊ¼µ½µÚy-1ÏÂ±ê
##description="Our young"
##d1=description[0]
##print("d1:   {0}".format(d1))
##d2=description[8]
##print("d2:   {0}".format(d2))
##d3=description[:3]
##print("d3:   {0}".format(d3))
##d4=description[3:]
##print("d4:   {0}".format(d4))
##d5=description[3:6]
##print("d5:   {0}".format(d5))

#########################       ×Öµä    ##############
##ÔÚÑ­»·ÖÐ£¬dictµÄÃ¿¸ö¼ü£¬±»ÌáÈ¡³öÀ´£¬¸³Óè¸økey±äÁ¿¡£
##Í¨¹ýprintµÄ½á¹û£¬ÎÒÃÇ¿ÉÒÔÔÙ´ÎÈ·ÈÏ£¬dicÖÐµÄÔªËØÊÇÃ»ÓÐË³ÐòµÄ¡£
##dic = {'lilei': 90, 'lily': 100, 'sam': 57, 'tom': 90}
##for key in dic:
##    print dic[key]


#########################       Òì³£´¦Àí    ##############
##re = iter(range(5))
##
##try:
##    for i in range(100):
##        print re.next()
##except StopIteration:
##    print 'here is end ',i
##
##print 'HaHaHaHa'
##
##print 'Lalala'
##raise StopIteration #Å×³öÒì³£
##print 'Hahaha'


#########################   Öµ´«µÝ¸úÖ¸Õë´«µÝ   #############
##############  ±í¡¾¡¿Ê¹ÓÃµÄÊÇÖ¸Õë´«µÝ£¬±äÁ¿aÊÇÖµ´«µÝ   #############
##a = 1
##
##def change_integer(a):
##    a = a + 1
##    return a
##
##print change_integer(a)
##print a
##
###===(PythonÖÐ "#" ºóÃæ¸úµÄÄÚÈÝÊÇ×¢ÊÍ£¬²»Ö´ÐÐ )
##
##b = [1,2,3]
##
##def change_list(b):
##    b[0] = b[0] + 1
##    return b
##
##print change_list(b)
##print b


##def fillData32bits(byteArray, data32bits):
##    byteArray.append((data32bits & 0x000000FF))
##    byteArray.append((data32bits & 0x0000FF00) >> 8)
##    byteArray.append((data32bits & 0x00FF0000) >> 16)
##    byteArray.append((data32bits & 0xFF000000) >> 24)
##    return byteArray
##
##bcaData = bytearray()
##fillData32bits(bcaData, 0xffffffff)
##    bcaFilePath = os.path.join(bl.vectorsDir, 'BCA.dat')
##    fileObj = open(bcaFilePath, 'w+')
##    fileObj.write(bcaData)
##    fileObj.close()
##    return bcaFilePath

############################ÌáÊ¾¿ò#######################
##import Tkinter
##import tkMessageBox
##

##def show():
##    tkMessageBox.showinfo(title='aaa', message='bbb')
## 
##def creatfram():
##    root = Tkinter.Tk()
##    b = Tkinter.Button(root, text="¹ØÓÚ", command=show)
##    b.pack()
##    root.mainloop()
##    root.exit()
##
##    
## 
##creatfram()


##from Tkinter import *
##
##from tkMessageBox import *
##
####if askyesno('Verify', 'Really quit?'):
####
####        #showwarning('Yes', 'Not yet implemented')
####        pass
##
##
##def answer():
##
##    #showerror("Answer", "Sorry, no answer available")
##    print ('error')
##
##
##def callback():
##
####    if askyesno('Verify', 'Really quit?'):
####
####        #showwarning('Yes', 'Not yet implemented')
####        pass
####
####    else:
####
####        showinfo('No', 'Quit has been cancelled')
####
##
##    pass
##Button(text='Quit', command=callback).pack(fill=X)
##
##Button(text='Answer', command=answer).pack(fill=X)
##
###mainloop()

# import wx
# class App(wx.App):
#     def OnInit(self):
#        dlg=wx.MessageDialog(None,"Is this the coolest thing ever!",
#        "MessageDialog",wx.YES_NO|wx.ICON_QUESTION)
#        result=dlg.ShowModal()
#        dlg.Destroy()
# app=App()
# app.MainLoop()

############################serial###################################
# import serial
# 
# cmd = "help\n"
# ser = serial.Serial('com9',115200,timeout = 0.01)
# ser.write(cmd)
# # str = ser.readall()
# #     #n = ser.inWaiting()
# #     #str = ser.read(n)
# # if(str):
# #     print str
# while 1:
#     str = ser.readall()
#     #n = ser.inWaiting()
#     #str = ser.read(n)
#     if(str):
#         print str  
#         
# #SPLITµÄ×÷ÓÃÊÇÎªÁËËµÃ÷ÕÒµ½×Ö·û´®¡°=¡·¡±
#     if (str.split("version")[0]):
#         break
# 
# ser.close()

# import time
# 
# # time1 = time.clock()
# # print "time1 : %d"  %time1
# # time.sleep(3)
# # time2 = time.clock()
# # print "time2 : %d"  %time2
# 
# d = {'a':1, 'b':2}
# print d['a']
# 
# c = [0,1,2,3,4,5]
# print c[2:]

##############################file ½«binÎÄ¼þ¼ÓÉÏ0x×ª»¯ÎªÎÄ±¾ÎÄ¼þ ###################################
# import os
# import array
# file = "C:/Users/b57252/Desktop/ivt_flashloader.bin"
# convertFile = "C:/Users/b57252/Desktop/ivt_flashloader_hex.txt"
# file_object = open(file,'rb')
# file_convert = open(convertFile,'w+')
# # TempArr = array.array('c')
# TempArr = []
# TempArr = file_object.read(16)
#  
# s = 0
# while TempArr:
#     for i in range(len(TempArr)):
#         value = ord(TempArr[i])
#         s = s + 1       
#         if value < 16:
#             value_temp = hex(value)
#             value_temp =  str(value_temp).split('0x',1)
#             value_write = '0x' + '0' + value_temp[1] + ','
#         else:   
#             value_temp = hex(value)
#             value_temp =  str(value_temp).split('0x',1)
#             value_write = '0x'  + value_temp[1] + ','
#              
#         if (i/15 == 1):
#     #             file_convert.write(hex(ord(TempArr[i])) + ',' + '\n')
#             file_convert.write(value_write + '\n')
#         else:
#     #             file_convert.write(hex(ord(TempArr[i])) + ',')
#             file_convert.write(value_write)
#     TempArr = file_object.read(16)
#      
# file_convert.write('\ntotal counter:')
# file_convert.write(str(s)+'\n')
#  
# print s
#  
# file_object.close()
# file_convert.close()


# heh = "hello"
# list = [1,2,3,4,'a','b']
# 
# a = 10
# if (a<20 and a>1):
#     print list[1:len(list):2]

# class superList(list):
#     def __sub__(self,b):
#         a = self[:]
#         b = b[:]
#         while len(b) > 0:
#             element_b = b.pop()
#             if element_b in a:
#                 a.remove(element_b)
#         return a
#     
# print superList([1,2,3]) - superList([3,4])
# 
# print dir(list)

# dic = {'a':1,'b':2, 'c':3}
# print dir(dic)
# 
# for s in dic:
#     print dic[s]

# def func(a,b,c):
#     print a,b,c
# 
# args = (1,2,3)
# print func(*args)


# a = (1,2,3)
# b = [1,2,3]
# print type(a), type(b)
# 
# def func(**arg):
#     print type(arg)
#     print arg
# 
# func(a=1,b=2,c=3)

# ´«Èë²ÎÊýµÄ´¦Àí
# import sys,getopt
# 
# def main():
#     args = '-a aa -b bb'
#     opt,args = getopt.getopt(args.split(), 'a:b:')
#     print opt
#     #options = dict(opt)
#     #print options['-a']
#     for a,b in opt:
#         if a == '-a':
#             opt_a = b
#         elif a == '-b':
#             opt_b = b
#         else:
#             print "nothing"
#     print opt_a,opt_b
#         
#     
#     
# if __name__ == "__main__":
#     main()

#loging ·½Ê½logÊä³ö
# import logging
# 
# def main():
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
#                         datefmt='%a, %d %b %Y %H:%M:%S',
#                         filename='C:/Users/b57252/Desktop/log.txt',
#                         filemode='w')
#     
#     console = logging.StreamHandler()
#     console.setLevel(logging.DEBUG)
#     formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#     console.setFormatter(formatter)
#     logging.getLogger('').addHandler(console)
#     logging.debug("debug info")
#     logging.info("haha")
#     logging.warning("warning")
#     logging.error("error")
#     logging.critical("critical")
#     
# 
# 
# if __name__ == "__main__":
#     main()

# dic/dic
# def main():
#     dic_header = {
#                   'dic1' : {
#                                 'a':'1',
#                                 'b':'2',
#                            }
#                   }
#      
#     for v, i in dic_header['dic1'].items():
#         print v,i
#     
#     
#     print dic_header['dic1'].items()
#     print 'hah'
#     
# 
# 
# if __name__ == "__main__":
#     main()



# import os

# def main(): 
    # flag = 1
    # KeyWord = ["MCU A","MCU B","MCU C","MCU D"]
    # while flag:
       # # os.system('zmjobs | tee lock.txt')
        # with open('lock.txt', 'r') as file:
            # for key in KeyWord:
                # while True:
                    # s = file.readline()
                    # if(key in s):
                        # break
                # s = file.readline()
                # s = file.readline()
                # if ("No job found" in s):
                    # print 'idle card is: ' + key
                    # if (key == "MCU A"):
                        # os.system('python ./zb_tb.py zebu11')
                    # elif (key == "MCU B"):
                        # os.system('python ./zb_tb.py zebu21')
                    # elif (key == "MCU C"):
                        # os.system('python ./zb_tb.py zebu31')
                    # elif (key == "MCU D"):
                        # os.system('python ./zb_tb.py zebu41')
                    # flag = 0
                    # break
                # # else:
                    # # while True:
                        # # s = file.readline()
                        # # if('SUBMIT_TIME' in s):
                            # # print 'go to find idle zebu card'
                            # # break
# if __name__ == '__main__':
    # main()
    
    
    
# import os
# 
# def main(): 
#     flag = 1
#     KeyWord = ["MCU A","MCU B","MCU C","MCU D"]
#     while flag:
#         os.system('zmjobs | tee lock.txt')
#         with open('lock.txt', 'r') as file:
#             while True:
#                 s = file.readline()  
#                 print s             
#                 if ("No job found" in s):
#                     s = file.readline()
#                     s = file.readline()            
#                     if ("MCU B" in s):
#                         print "MCU A is idle"
#                         os.system('python ./zb_tb.py zebu11')
#                     elif ("MCU C" in s):
#                         print "MCU B is idle"
#                         os.system('python ./zb_tb.py zebu21')
#                     elif ("MCU D" in s):
#                         print "MCU C is idle"
#                         os.system('python ./zb_tb.py zebu31')
#                     elif ("" == s):
#                         print "MCU D is idle"
#                         os.system('python ./zb_tb.py zebu41')
#                     flag = 0           
#                     break
#                 elif ("" == s):
#                     os.system('ls | tee lock.txt')
#                     break
# if __name__ == '__main__':
#     main()
    
    
# detect idle zebu card    
# import os
#  
# def main(): 
#     flag = 1
#    # KeyWord = ["MCU A","MCU B","MCU C","MCU D"]
#     while flag:
#         os.system('zmjobs | tee lock.txt')
#         with open('lock.txt', 'r') as file:
#             while True:
#                 s = file.readline()  
#                 #print s             
#                 if ("No job found" in s):
#                     s = file.readline()
#                     s = file.readline()            
#                     if ("MCU B" in s):
#                         print "MCU A is idle"
#                         os.system('python ./zb_tb.py zebu11')
#                     elif ("MCU C" in s):
#                         print "MCU B is idle"
#                         os.system('python ./zb_tb.py zebu21')
#                     elif ("MCU D" in s):
#                         print "MCU C is idle"
#                         os.system('python ./zb_tb.py zebu31')
#                     elif ("" == s):
#                         print "MCU D is idle"
#                         os.system('python ./zb_tb.py zebu41')
#                     flag = 0           
#                     break
#                 elif ("" == s):
#                     file.close()
#                     break
# if __name__ == '__main__':
#     main()


# pipe

# import subprocess
# import json
# import time
# def test():
        
        # cmdlist = ['dir','ls','ver','help','ipconfig']
        # cmd = 'dir'
        # p = subprocess.Popen(cmd, 0, None, None, subprocess.PIPE, subprocess.STDOUT, shell=True)
# #         p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # sout,serr= p.communicate()


        # with open("lock.txt", 'w') as file:
            # file.write(sout)
        # file.close()

        # print sout
        # print "========================"
        
        # print time.localtime()

        
# #         json_file = json.loads(sout)
# #         print "*****************************"
# #         print json_file
        
        
# #         if Helper.interact_run.if_timeout:
# #             ret_val = 'Timeout'
# #         else:
# #             ret_val = p.returncode
# #         ret_info = sout + serr
# #         logging.info('ret_val = %s' % ret_val)
# #         logging.info('ret_info = %s' % ret_info)
# #         if ret_val == 0:
# #             try:
# #                 ret_info = json.loads(ret_info)
# #             except Exception, e:
# #                 pass
# #         else:
# #             pass
# #         print 'ret_val = %s' % ret_val
# #         print 'ret_info = %s' % ret_info
# #         return (ret_val, ret_info)
    
# if __name__ == "__main__":
    # test()
                    



# #encoding:utf-8
# from multiprocessing import Process
# import os, time, random
# 
# 
# def r1(process_name):
#     for i in range(5):
#         print process_name, os.getpid()     #´òÓ¡³öµ±Ç°½ø³ÌµÄid
#         time.sleep(random.random())
# def r2(process_name):
#     for i in range(5):
#         print process_name, os.getpid()     #´òÓ¡³öµ±Ç°½ø³ÌµÄid
#         time.sleep(random.random()*4)
#  
# if __name__ == "__main__":
#         print "main process run...", os.getpid()
# 
#         p1 = Process(target=r1, args=('process_name1', )) 
#         p2 = Process(target=r2, args=('process_name2', )) 
#  
#         p1.start()
#         p2.start()
#         p1.join()
# #         p2.join()    
#         print "main process runned all lines...", os.getpid()


# import multiprocessing as mul
# 
# def proc1(pipe):
#     pipe.send('hello')
#     print('proc1 rec:',pipe.recv())
# 
# def proc2(pipe):
#     print('proc2 rec:',pipe.recv())
#     pipe.send('hello, too')
# 
# 
# 
# if __name__ == '__main__':
# # Build a pipe
#     pipe = mul.Pipe()
#     
#     # Pass an end of the pipe to process 1
#     p1   = mul.Process(target=proc1, args=(pipe[0],))
#     # Pass the other end of the pipe to process 2
#     p2   = mul.Process(target=proc2, args=(pipe[1],))
#     p1.start()
#     p2.start()
# #     p1.join()
# #     p2.join()

# Written by Vamei
# import os
# import multiprocessing
# import time
# #==================
# # input worker
# def inputQ(queue):
#     info = str(os.getpid()) + '(put):' + 'str(time.time())'
#     queue.put(info)
#     print 'input' + str(os.getpid())
# 
# # output worker
# def outputQ(queue,lock):
#     info = queue.get()
# #     lock.acquire()
#     print (str(os.getpid()) + '(get):' + info)
# #     lock.release()
#     
# if __name__ == '__main__':
#     #===================
#     # Main
#     record1 = []   # store input processes
#     record2 = []   # store output processes
#     lock  = multiprocessing.Lock()    # To prevent messy print
#     queue = multiprocessing.Queue()
#     
#     # input processes
#     for i in range(10):
#         process = multiprocessing.Process(target=inputQ,args=(queue,))
#         process.start()
#         record1.append(process)
#         
#     for p in record1:
#         p.join()
#     
#     # output processes
#     for i in range(10):
#         process = multiprocessing.Process(target=outputQ,args=(queue,lock))
#         process.start()
#         print i
#         record2.append(process)      
# #     queue.close()  # No more object will come, close the queue
#      
#     for p in record2:
#         p.join()
#         
#     print 'main'


# ±éÀúÎÄ¼þ¼Ð

import os
# def walk_dir(dir,fileinfo,topdown=True):
#     dir_count =0
#     file_count =0
#     for root, dirs, files in os.walk(dir, topdown):
# #         print '--------root-------------'
# #         print root
# #         print '--------dirs-------------'
# #         print dirs
# #         print '--------files-------------'
#         print files
#         for name in dirs:
#             print(os.path.join(root,name)) 
#             fileinfo.write('  ' + os.path.join(root,name) + '\n')   
#             dir_count = dir_count + 1   
#         for name in files:
#             print(os.path.join(root,name))
#             fileinfo.write(os.path.join(root,name) + '\n')
#             file_count = file_count +1
#     print 'dir_count', dir_count
#     print 'file_count', file_count
          
        
# dir = raw_input('please input the path:')
# dir = 'C:\\Users\\b57252\\Desktop\\previous_log\\ROM_EMMC_USER_2ND\\MMC_8BITDDR_FAST_2nd_of0.txt'
# dir = 'C:\\Users\\b57252\\Desktop\\previous_log'
# # print os.path.splitext(dir)[1]
# count = 0
# for root, dirs, files in os.walk(dir):
#     for name in files:
#         file_router = os.path.join(root,name)
#         file_type = os.path.splitext(file_router)[1]
#         if '.txt' == file_type:
#             count = count +1
#         print file_router
#         print file_type
# print count
# 
# 
# print os.path.abspath(dir).replace('\\','/')
# fileinfo = open('list.txt','w')
# walk_dir(dir,fileinfo)


# import logging
# from lib import log
# from lib import send_command
# def main(): 
#     logging.info('=========================')
#     send_command.send_command('dir')
#     get_string = send_command.get_string('.project',10)
#     logging.info('get string %s',get_string)
#     send_command.find_string('config')
#     send_command.send_command('ls')
#     send_command.find_string('log.py')
#     send_command.find_string('11.py')
# 
# if __name__ == "__main__":
#     main()


# import os
# import multiprocessing
# import time
# #==================
# # input worker
# def inputQ(queue):
#     info = str(os.getpid()) + '(put):' + 'str(time.time())'
#     queue.put(info)
#     print 'input' + str(os.getpid())
# 
# # output worker
# def outputQ(queue,lock):
#     info = queue.get()
# #     lock.acquire()
#     print (str(os.getpid()) + '(get):' + info)
# #     lock.release()
#     
# if __name__ == '__main__':
#     #===================
#     # Main
#     record1 = []   # store input processes
#     record2 = []   # store output processes
#     lock  = multiprocessing.Lock()    # To prevent messy print
#     queue = multiprocessing.Queue()
#     
#     # input processes
#     for i in range(10):
#         process = multiprocessing.Process(target=inputQ,args=(queue,))
#         process.start()
#         print 'input',i
#         record1.append(process)
#     
# #     # output processes
# #     for i in range(10):
# #         process = multiprocessing.Process(target=outputQ,args=(queue,lock))
# #         process.start()
# #         print 'output', i
# #         record2.append(process)
# 
#     
# 
#     
#     for p in record1:
#         p.join()
#         
#     print os.getpid(), queue.get()    
#     print os.getpid(), queue.get() 

    
#     queue.close()  # No more object will come, close the queue
    
#     for p in record2:
#         p.join()


# import os
# import multiprocessing
# import time
# #==================
# # input worker
# def worker(running_flag, queue):
# #     info = str(os.getpid()) + '(put):' + 'str(time.time())'
# #     queue.put(info)
#     print os.getpid() , 'worker ' ,running_flag.value
#     info = str(os.getpid()) + 'send from worker'
# #     queue.put(info)
# 
# 
# # output worker
# def loger(running_flag, queue):
#     print os.getpid() , 'loger ' , running_flag.value
# #     print os.getpid() , 'loger get: ' , queue.get()
# #     running_flag.value = running_flag.value + 2
#     
# def doger(running_flag,queue):
#     while True:
#         str = queue.get(timeout = 20)
#         print 'dog got', str
#         if str == 'quit':
#             print os.getpid(), ' dog ','got quit message'
#             break
#     print 'break successfully'
#         
# 
# 
# work_list = []
# log_list = []
#      
# if __name__ == '__main__':
#     
#     queue = multiprocessing.Queue()
#     running_flag = multiprocessing.Value('i', 1)
#     for i in range(10):
#         work = multiprocessing.Process(target=worker, args=(running_flag, queue)) 
#         work_list.append(work)
#         
#     for i in range(10):
#         log  = multiprocessing.Process(target=loger, args=(running_flag, queue))
#         log_list.append(log)
#     
#     dog = multiprocessing.Process(target=doger, args=(running_flag, queue)) 
#     dog.start()
#         
#     for i in work_list:
#         i.start() 
#         i.join()
# #         if i == work_list[8]:
# #             queue.put('quit')
# #             print 'quit has been send'
# #         i.join()
#     
#     for i in log_list:
#         i.start()
# #         i.join()
#         
#     queue.put('hah')
# 
#     queue.put('quit')
#         
# 
# 
#     print 'main'

# import os
# import multiprocessing
# import time
# import subprocess
# 
# # buffer = ''
# 
# def dump_log():
#     while True:
#         print 'worker'
# 
# def worker(running_flag, queue, pp):
# #     global buffer
#     print 'entring into worker'
#     p = subprocess.Popen('dir', 0, None, subprocess.PIPE, subprocess.PIPE, None, shell=True)
#     (sout, serr) = p.communicate()
#     if sout:
#         pp.send(sout)
# 
# # output worker
# def loger(running_flag, queue, pp):
#     print 'loger id is :', os.getpid()
#     buffer = pp.recv()
#     while True:
# #         buffer = queue.get()
#         if buffer != '':     
#             print 'wtite buffer'
#             print buffer
#             with open('result/log.txt', 'w+') as f:
#                 f.write(buffer)
#                 f.write('--------test--------------------------')
#             if 'result' in buffer:
#                 queue.put('quit')
#         
# def doger(running_flag,queue):
#     while True:
#         print 'dog'
#         
# 
# if __name__ == '__main__':
# 
#     
#     queue = multiprocessing.Queue()
#     running_flag = multiprocessing.Value('i', 1)
#     pp = multiprocessing.Pipe()
#     
#     work = multiprocessing.Process(target=worker, args=(running_flag, queue, pp[0]))
#     log  = multiprocessing.Process(target=loger, args=(running_flag, queue, pp[1]))    
#     dog = multiprocessing.Process(target=doger, args=(running_flag, queue)) 
#     
#     
#     work.start()
# #     work.join(timeout=2)
#     log.start()
#     
#     
# #     dog.start()
#     
# #     time.sleep(2)
# #     work.terminate()
# #     log.terminate()
# #     dog.terminate()
#    
# #     while True:
# #         if buffer:
# #             print 'main:',buffer
#             
#     
#     while True:
#         print 'main proces'
#         msg = queue.get()
#         print 'got message ', msg
#         if msg == 'quit':
#             work.terminate()
# #             work.join()
#             log.terminate()
#             print 'terminate process'
#             break
# #             log.join()
# #             dog.terminate()
# #             dog.join()
#     
# 
#     print 'main'
    
    
#计算保险
# price = raw_input('please input price of insurance:')
# price = int(price)
# # price = 3302
# year  = raw_input('please input how many years that insurance not used:')
# year = int(year)
# time  = raw_input('please input how much times does insurance used:')
# time = int(time)

# calculate = {
#              0:{
#                 0: 0.85,
#                 1: 1,
#                 2: 1.25,
#                 3: 1.5,
#                 4: 1.75,
#                 5: 2
#                },
#              1:{
#                 0: 0.7,
#                 1: 1,
#                 2: 1.25,
#                 3: 1.5,
#                 4: 1.75,
#                 5: 2
#                 },
#              2:{
#                 0: 0.6,
#                 1: 1,
#                 2: 1.25,
#                 3: 1.5,
#                 4: 1.75,
#                 5: 2
#                 },
#              }

# if year>2:
#     year = 2

# price_for_next_year = price*calculate[year][time]
# print "insurance price for next year:", price_for_next_year
# # price_next_year = 3000 * calculate[0][0]

# if time==0:
#     price_for_next_year_not_using_insurance = price*calculate[year][time]
#     print "insurance price for next year if not using insurance:", price_for_next_year_not_using_insurance
#     print "insurance price for the year after next if not using insurance:", price*calculate[year+1][time]
# else: 
#     price_for_next_year_not_using_insurance = price*calculate[year][time-1]
#     print "insurance price for next year if not using insurance", price_for_next_year_not_using_insurance
    
# print 'price difference if using insurance or not',price_for_next_year-price_for_next_year_not_using_insurance
  
# print "HaHaHaHa"

# import os
# # os.environ['test'] = '123'
# hah = '11'
# print os.environ.get('Python')
# print locals()

# print '=================='
# print globals()

# import ConfigParser
# config = ConfigParser.SafeConfigParser()
# config.read('config.ini')

# print config.get('config','core')
# print config.get('speed','dd_speed')
# print os.environ.items()

# import os
# print os.popen("dir").read()

#**********************testing pytest conftest
# import pytest
# 
# @pytest.fixture(autouse=True)
# def ss(request):
#     pytest.skip("should not be tested")
# 
# def test(bl):
#     print 'hah'
#     bl.output('==============happy new year==================')


#****************************re ***********************************
# import collections
# import os
# import re
# file = r"E:\Doc\NewFeatures\ROM\8QXP\B0\case_list\unit_tset\log\ROM_UNIT_TEST_BOOT_FLOW_TEST.txt"
# with open(file,'r') as f:
#     content = f.read()
# 
# 
# 
# orderDict = dict(collections.OrderedDict())
# 
# dict = {'hah':{'a':'1','b':'2'}}
# print dict['hah']['a']
# 
# list = ['hah','heh','xixi']
# print list[-2]
# 
# 
# 
# pattern_match = 'done'
# start = content.find(pattern_match,0)
# print start
# 
# p = re.compile(pattern_match, re.I|re.M)
# print [match.start() for match in p.finditer(content)]
# 
# print match
# 
# 
# # content = '''A value is 1, b value is 2, c value is 3, d value is 4'''
# 
# file = r"E:\Doc\NewFeatures\ROM\8QXP\B0\case_list\unit_tset\log\ROM_LOCK_FUSE\ALL_LOCKED_TEST.txt"
# with open(file,'r') as f:
#     content = f.read()
# dict = {}
# result = re.findall('BootROM_SCU: register after setting .* value is .*', content)
# print result
# 
# for element in result:
#     print '---------\n'
#     print element
#     element_list = element.split(' ')
# #     print element_list
#     
#     dict[element_list[4]] = element_list[7]
#     
# value = dict['DSC_CA35']
# print type(value)
# 
# value = eval(dict['DSC_CA35'])
# print type(value)
# print value
# print bin(value)[-4:-1]


#*********************hex convert
# test = '0x1003'
# print type(eval(test))
# bin = bin(eval(test))
# print bin
# print bin[2:]
# print type(bin)
# print int(bin,2)

#********************yaml***********************
# import os
# import yaml
# import json
# 
# pattern_info_dict = {
#                         'ROM_EMMC_BOOT0&Boot0_4-bit': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_BOOT0&Boot0_4-bit_Fast-boot_ACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_BOOT0&Boot0_4-bit_Fast-boot_NOACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_BOOT0&Boot0_4-bit-DDR': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_BOOT0&Boot0_4-bit-DDR_Fast-boot_ACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_BOOT0&Boot0_4-bit-DDR_Fast-boot_NOACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_BOOT0&Boot0_8-bit': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_BOOT0&Boot0_8-bit_Fast-boot_ACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_BOOT0&Boot0_8-bit_Fast-boot_NOACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_BOOT0&Boot0_8-bit-DDR': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_BOOT0&Boot0_8-bit-DDR_Fast-boot_ACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_BOOT0&Boot0_8-bit-DDR_Fast-boot_NOACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_4-bit': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_4-bit_Fast-boot_ACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_4-bit_Fast-boot_NOACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_4-bit-DDR': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_4-bit-DDR_Fast-boot_ACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_4-bit-DDR_Fast-boot_NOACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_8-bit': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_8-bit_Fast-boot_ACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_8-bit_Fast-boot_NOACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_8-bit-DDR': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_8-bit-DDR_Fast-boot_ACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_EMMC_USER&BootU_8-bit-DDR_Fast-boot_NOACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_SD&SD_SDR12': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_SD&SD_SDR12_Fast-boot_ACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_SD&SD_SDR25': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_SD&SD_SDR25_Fast-boot_ACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_SD&SD_SDR50': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']},
#                         'ROM_SD&SD_SDR50_Fast-boot_ACK': {'no_pattern': ['FAIL'], 'pattern': ['bt_system_init done', 'init image success']}
#                     }
# 
# main_path = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')
# result_path = os.path.join(main_path,'result')
# yaml_file = os.path.join(result_path,'result.yaml')
# json_file = os.path.join(result_path, 'result.json')
# if (True == os.path.isfile(yaml_file)):
#     os.remove(yaml_file)
# else:
#     pass

# with open(json_file, 'w') as f:
#     print json.dump(pattern_info_dict, f, sort_keys=True)
# #     content = f.read()
#     f.close()
#     
# print json.dumps(pattern_info_dict, sort_keys=True, indent=4, separators=(',', ': ') )
    
# with open(yaml_file, 'r') as f:
#     content = yaml.load(f)
#     yaml.dump(pattern_info_dict, f)
#     f.close() 

#**************************blhost********************************

# import subprocess
# import json
# import re
# 
# comport = 'com10 '
# blhost = r'C:\Users\nxa28190\Desktop\Tools\blhost\win\blhost.exe '
# command = [blhost,'-p ','-j ' ,'-- ' ,'get-property 1']
# 
# command.insert((command.index('-p ')+1),comport) 
# command = [str(x) for x in command]
# command = ''.join(command)
# print command
# 
# # command = blhost + ' -p com10  -j -- get-property 1'
# 
# 
# 
# class blhost(object):   
#     def parse(self, result):
#         json_result = result[result.find('{') : result.rfind('}')+1]
#         if len(json_result):
#             pass
#         else:
#             print 'blhost has no output'
#             return
#         actualResults = json.loads(json_result)
#         print actualResults['status']['value'],actualResults['response']
#         print type(actualResults['status']['value'])
#         print type(actualResults['response'])
# 
#     def send_command(self,cmd):
#         p = subprocess.Popen(cmd, 0, None, subprocess.PIPE, subprocess.PIPE, None, shell=True)
#         (sout, serr) = p.communicate() 
#         print sout
#         self.parse(sout)
#        
#             
# if __name__ == '__main__':
#     pass
#     a = blhost()
#     a.send_command(command)
    
 
#enumerate
# test_list = ['a','b','c']
# 
# test_list = [(i+ 'dd')for i in test_list]
# 
# for num,content in enumerate(test_list):
#     print num,content 
 
#spider 
# -*- coding: utf-8 -*-
import sys
import re
import requests
import urllib2
from lxml import  etree
string = "adbdddddbaaaaaab"
  
# result =  re.findall('a.*?b',string)
# print result
# 
# def Write_File(content):
#     with open('content.txt','w+') as fp:
#         for items in content:
#             print items[0].encode("utf8")
#             fp.write("%s\t\t%s\n" %(items[0].encode("utf8"),items[1].encode("utf8")))
# 
# def Page_Info(myPage):
#     '''Regex'''
#     mypage_Info = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>', myPage, re.S)
#     return mypage_Info
# 
# 
# start_url = "http://news.163.com/rank/"
# myPage = requests.get(start_url).content.decode("gbk")
# 
# result = Page_Info(myPage)
# Write_File(result)
# for items in result:
#     print items[0],items[1]
#     write_file(items[0].encode("utf8"), items[1].encode("utf8"))
# print result[0][0]
# print result[0][1]
# print Page_Info(myPage)
# myPage.encode('UTF-8')
# write_file(myPage)



def Page_Info(page):
    # myPage_Info = re.findall(r'div class="titleBar" id=.*?><h2>(.*?)</h2><div class="more"><a href="(.*?)">' , page, re.S)
    my_Page = etree.HTML(page)
    title = my_Page.xpath("//div/h2/text()")

    for item in title:
        print item
    return title

def Write_File(content):
    with open("content.txt","w+") as fp:
        for s in content:
            fp.write("%s\t\t%s\n" %(s[0] , s[1]) )

if __name__ == "__main__":
    start_url = "http://news.163.com/rank/"
    # myPage = requests.get(start_url).content.decode("gbk")
    myPage = requests.get(start_url).content.decode("gbk")
    # print myPage
    # print sys.getdefaultencoding()
    content = Page_Info(myPage)
    Write_File(content)








    

















    
    
        


     
