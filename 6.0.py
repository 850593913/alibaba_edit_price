from tkinter import * #窗口
from tkinter.filedialog import askdirectory #选择文件夹
from tkinter.filedialog import askopenfilename #选择文件
import os #打开文件，获取路径
import csv #csv文件
import tkinter.messagebox #弹窗
import win32api,win32con #弹窗
import psutil #用于判断进程是否存在
import pandas #用于xlsx转换
p=os.getcwd() #获得程序路径
#将xlsx文件转换为csv文件
def xlsx_to_csv():
    data_xlsx = pandas.read_excel(xlsx_replace, index_col=0)
    data_xlsx.to_csv(p+'\\'+'1.csv', encoding='utf-8')
#判断photoshop是否打开
def judgeprocess():
    isopen=0
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == 'Photoshop.exe':
            isopen=1
            break
    else:    
        print("not found")
        isopen=0
    return isopen

#csv路径
def selectExcel():
    xlsx_=askopenfilename()
    xlsx.set(xlsx_)
    global xlsx_replace
    xlsx_replace=str(xlsx.get()).replace('/','//')
#保存路径
def selectSave():
    save_=askdirectory()
    save.set(save_)
    global save_replace
    save_replace=str(save.get()).replace('/','//')
#建立窗口
root = Tk()
root.resizable(0,0)
#可变字符串
xlsx=StringVar()
save=StringVar()
#主项目
def project():
    try:
        xlsx_to_csv() #将xlsx转换为csv
        with open(p+'\\'+'1.csv') as f:
            reader=csv.reader(f)
            rows=[row for row in reader]
            ready=win32api.MessageBox(0, "包含"+str(len(rows))+'个型号\n确定要执行吗', "提醒",win32con.MB_YESNO)
            if ready==6: #判断是否确定要执行程序
                if judgeprocess()==1: #判断photoshop是否打开，等于1表示打开了，0表示没有打开
                    #在桌面记录下程序路径
                    mainpath=open('C:\\Users\\Administrator\\Desktop\\mainpath.txt','w',encoding='utf-8')
                    mainpath.write(p) #写入p=os.getcwd()
                    mainpath.close() 
                    #在同级目录记录数据
                    file_1=open('data.txt','w',encoding='utf-8')
                    for i in rows:
                        file_1.write(i[0]+','+i[1]+'\n') 
                    file_1.close()
                    #在同级目录记录保存路径
                    file_2=open('save.txt','w',encoding='utf-8')
                    file_2.write(save_replace)
                    file_2.close()
                    os.startfile('test.jsx') #运行脚本
                    # win32api.MessageBox(0, "完成", "提醒",win32con.MB_OK)                                        
                else:
                    win32api.MessageBox(0, "photoshop未打开", "提醒",win32con.MB_OK)
                    win32api.MessageBox(0, "程序终止", "提醒",win32con.MB_OK)                                        
            else:
                win32api.MessageBox(0, "程序终止", "提醒",win32con.MB_OK)          
    except Exception as ex:
        print(ex)
        tkinter.messagebox.showinfo("Alert",ex) #错误弹窗
        win32api.MessageBox(0, "程序终止", "提醒",win32con.MB_OK)
#界面窗口按钮，输入框，标签
#csv文件路径
Label(root,text = "Excel文件路径:").grid(row = 1, column = 0)
Entry(root).grid(row = 1, column = 1)
Button(root, text = "选择文件", command = selectExcel).grid(row = 1, column = 2)
#保存路径
Label(root,text = "保存路径:").grid(row = 2, column = 0)
Entry(root).grid(row = 2, column = 1)
Button(root, text = "选择路径", command = selectSave).grid(row = 2, column = 2)
#执行主项目
Button(root, text = "执行", command = project).grid(row = 3, column = 2)

#主消息循环
root.mainloop()