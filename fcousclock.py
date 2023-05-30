import time
import math
import random
import datetime
import requests
import tkinter as tk
from io import BytesIO
from threading import Thread
from PIL import Image, ImageTk
from tkinter import messagebox
 
 
class Clock():
    def __init__(self, master, x, y, radius):
        self.centerX = x
        self.centerY = y
        self.radius = radius
        self.canvas = master
        self.id_lists = []
        self.hourHandRadius = self.radius * 1.0 / 4  # 指针长度
        self.minHandRadius = self.radius * 2.0 / 3  # 分针长度
        self.secHandRadius = self.radius * 4.0 / 5  # 秒针长度
        self.timeVar = tk.StringVar()
        # 绘制钟盘上的刻度
        r1 = self.radius - 5
        r2 = self.radius
        for i in range(1, 61):
            rad = 2 * math.pi / 60 * i
            x1, y1 = self._getPosByRadAndRadius(self.centerX,self.centerY,rad, r1)
            x2, y2 = self._getPosByRadAndRadius(self.centerX,self.centerY,rad, r2)
            id = self.canvas.create_line(x1, y1, x2, y2)
            self.id_lists.append(id)
    def drawClockDial(self,num,m):
        # 绘制钟盘上的数字1-num
        r = self.radius - 15
        for i in range(1,num+1):
            rad = 2 * math.pi /num * i
            x = self.centerX + math.sin(rad) * r
            y = self.centerY - math.cos(rad) * r
            a=i*m
            id = self.canvas.create_text(x, y, text=str(a))
            self.id_lists.append(id)
        # 绘制钟盘上的刻度
        r1 = self.radius - 5
        r2 = self.radius
        for i in range(1, 61):
            rad = 2 * math.pi / 60 * i
            x1, y1 = self._getPosByRadAndRadius(self.centerX,self.centerY,rad, r1)
            x2, y2 = self._getPosByRadAndRadius(self.centerX,self.centerY,rad, r2)
            id = self.canvas.create_line(x1, y1, x2, y2)
            self.id_lists.append(id)
    # 获取刻度所在位置
    def _getPosByRadAndRadius(self,centerX,centerY, rad, radius):
        x = centerX + radius * math.sin(rad)
        y = centerY - radius * math.cos(rad)
        return (x, y)
    def showTime(self, tm):
        hour = tm.tm_hour % 12
        min = tm.tm_min
        sec = tm.tm_sec
        sec_rad = 2 * math.pi / 60 * sec
        min_rad = 2 * math.pi / 60 * (min + sec / 60.0)
        hour_rad = 2 * math.pi / 12 * (hour + min / 60.0)
        timeStr = '%d-%02d-%02d %02d:%02d:%02d' % (
            tm.tm_year, tm.tm_mon, tm.tm_mday, hour, min, sec)
        # self.timeVar.set(timeStr)
        hour_id = self._drawLine(self.centerX,self.centerY,hour_rad, self.hourHandRadius, 6)
        min_id = self._drawLine(self.centerX,self.centerY,min_rad, self.minHandRadius, 4)
        sec_id = self._drawLine(self.centerX,self.centerY,sec_rad, self.secHandRadius, 3)
        self.canvas.create_text(200,340,text=timeStr, font = "宋体 20",tag='a')
        return (hour_id, min_id, sec_id,'a')
    def _drawLine(self,centerX,centerY, rad, radius, width):
        x, y = self._getPosByRadAndRadius(centerX,centerY,rad, radius)
        id = self.canvas.create_line(centerX,centerY, x, y, width=width)
        return id
    def _deleteItems(self, id_lists):
        for id in id_lists:
            try:
                self.canvas.delete(id)
            except BaseException:
                pass
    def run1(self):
        def _run():
            while flag==1:
                tm = time.localtime()
                id_lists = self.showTime(tm)
                self.canvas.master.update()
                time.sleep(1)
                self._deleteItems(id_lists)
        thrd = Thread(target=_run)  # 创建新的线程
        thrd.run()  # 启动线程
    def run2(self):
        def _run():
            while flag==2:
                global tm;tm+=1
                id_lists = self.showTime2(tm)
                self.canvas.master.update()
                time.sleep(1)
                self._deleteItems(id_lists)
 
        thrd = Thread(target=_run)  # 创建新的线程
        thrd.run()  # 启动线程
    def showTime2(self, tm):
        sec = tm%60
        min=tm//60
        sec_rad = 2 * math.pi / 60 * sec
        min_rad = 2 * math.pi / 60 * (min + sec / 60.0)
        timeStr = '当前计时:%02d分%02d秒' % (min, sec)
        sec_id = self._drawLine(200,160,sec_rad,120, 3)
        sec_id1 = self._drawLine(200,90,min_rad,40, 5)
        self.canvas.create_text(200,340,text=timeStr, font = "宋体 20",tag='a')
        return (sec_id,sec_id1,'a')
    def run3(self):
        def _run():
            global tm,t;
            while flag == 3 and t<tm:
                t+= 1
                id_lists = self.showTime3(tm)
                self.canvas.master.update()
                time.sleep(1)
                self._deleteItems(id_lists)
        thrd = Thread(target=_run)  # 创建新的线程
        thrd.run()  # 启动线程
    def showTime3(self, tm):
        global tt
        tt-=1
        sec = t/tm* 2 * math.pi
        s=tt%60
        h=tt//3600
        m=tt//60-h*60
        sec_rad =sec
        timeStr = '当前计时:%02d时%02d分%02d秒' % (h,m,s)
        self.canvas.create_text(200, 320, text=timeStr, font="宋体 20", tag='a')
        return ('a')
 
def closeWindow():
    messagebox.showinfo(title="关不掉吧", message="想不到吧，气不气")
    return
 
# 建立窗口
window = tk.Tk()
window.title('时钟   by 113120190365陈思杰')
window.resizable(width=False, height=False)
window.geometry('400x600+1000+100')
window.protocol("WM_DELETE_WINDOW", closeWindow)
 
# 建立框架
canvas_Main = tk.Canvas(window,width=400,bg='white', height=600)
canvas_Main.pack()
response = requests.get('https://blog-static.cnblogs.com/files/csjsdyp/%E6%BB%A1%E5%88%86.gif')
load = Image.open(BytesIO(response.content))
render = ImageTk.PhotoImage(load)
canvas_Main.create_text(200,200,text='请在菜单栏选择\n模式进行调试', font="宋体 20")
ls=[]
# 模式选择函数
def forget():
    for i in ls:
        try:
            a=i+'.place_forget()'
            eval(a)
        except:
            pass
global flag;flag =0
# 时钟模式
def mode1():
    forget()
    global flag;flag =1;
    canvas_Main.delete('all')
    canvas_Main.create_oval(50, 10, 350, 310) #表盘绘制
    clock = Clock(canvas_Main, 200, 160, 150) #刻度绘制
    clock.drawClockDial(12,1) #数字绘制
    clock.run1()
# 秒表模式
def mode2():
    forget()
    global flag;flag = 2;
    global ls;ls = ["L2", "B21", "B22", "B23"]
    global tm;tm = 0;
    canvas_Main.delete('all')
    canvas_Main.create_oval(50, 10, 350, 310)
    canvas_Main.create_oval(150, 40, 250, 140)
    clock0 = Clock(canvas_Main, 200, 160, 150)
    clock1 = Clock(canvas_Main, 200, 90, 50)
    clock0.drawClockDial(12,5)
    clock1.drawClockDial(6,10)
    global a,b,num
    num=0
    a= clock0._drawLine(200,160,0,120, 3)
    b= clock1._drawLine(200,90,0,40, 5)
    def guiling():
        global num,a,b,tm, flag;
        num,flag, tm =0, 4, 0;
        L2.delete(0,"end")
        a=clock0._drawLine(200,160,0, 120, 3)
        b=clock1._drawLine(200,90,0, 40, 5)
    def begin():
        global flag,a,b;flag=2
        canvas_Main.delete(a,b)
        clock0.run2()
    def jilu():
        global tm,num
        num+=1
        sec = tm % 60
        min = tm // 60
        a="%03d %02d:%02d" % (num,min,sec)
        L2.insert("end",a)
    L2.place(x=130, y=370)
    global B21,B22,B23
    B21 = tk.Button(window,bd=1, text='归零', command=guiling)
    B21.place(x=130, y=500)
    B22 = tk.Button(window,bd=1, text='开始', command=begin)
    B22.place(x=180, y=500)
    B23 = tk.Button(window,bd=1, text='记录', command=jilu)
    B23.place(x=230, y=500)
# 倒计时模式
def mode3():
    forget()
    global ls,a,t,flag;
    flag = 3;t=0;
    ls=["B31","B32","L30","L31","L32","L33","E31","E32","E33"]
    clock0 = Clock(canvas_Main, 200, 160, 150)
    canvas_Main.delete('all')
    def show():
        global tm,tt,flag
        flag=3
        h = E31.get()
        m = E32.get()
        s = E33.get()
        if h=='':h=0
        if m=='':m=0
        if s=='':s=0
        tm=int(h)*60*60+int(m)*60+int(s);
        tt=tm
        E31.delete(0, "end")
        E32.delete(0, "end")
        E33.delete(0, "end")
        clock0.run3()
    def stop():
        global flag
        flag=4
    global B31,B32
    B31 = tk.Button(window, bd=1, text='Run', command=show,width=6)
    B32 = tk.Button(window, bd=1, text='Stop', command=stop,width=6)
    L30.place(x=90, y=60);
    L31.place(x=200, y=100)
    L32.place(x=200, y=140)
    L33.place(x=200, y=180)
    E31.place(x=120, y=100)
    E32.place(x=120, y=140)
    E33.place(x=120, y=180)
    B31.place(x=110,y=240)
    B32.place(x=170,y=240)
# 退出模式
def mode4():
    forget()
    global flag;flag =4;
    global ls;ls = ["L41", "B41", "B42"]
    canvas_Main.delete('all')
    L41.place(x=30, y=60)
    B41.place(x=130, y=400)
    B42.place(x=230, y=400)
def tongyi():
    window.destroy()
def butongyi():
    B42.place_forget()
    B42.place(x=random.randint(230, 300), y=random.randint(350,550))
 
# 控件定义
L2 = tk.Listbox(window, height=6)
L30 = tk.Label(window,font = "宋体 23",bg='white', text="请输入时间")
L31 = tk.Label(window,font = "宋体 20",bg='white', text="时")
L32 = tk.Label(window,font = "宋体 20",bg='white', text="分")
L33 = tk.Label(window,font = "宋体 20",bg='white', text="秒")
V1=tk.StringVar()
V2=tk.StringVar()
V3=tk.StringVar()
E31 = tk.Entry(window,font = "宋体 24", bd =2,width=4,textvariable=V1)
E32 = tk.Entry(window,font = "宋体 24", bd =2,width=4,textvariable=V2)
E33 = tk.Entry(window,font = "宋体 24", bd =2,width=4,textvariable=V3)
L41 = tk.Label(window, bg='white', image=render)
B41 = tk.Button(window,bd=1,text='同意',font = "宋体 15", command=tongyi)
B42 = tk.Button(window,bd=1,text='不同意',font = "宋体 15", command=butongyi)
# 建立菜单
menubar = tk.Menu(window)
menubar.add_command(label = "时钟", command =mode1)
menubar.add_command(label = "秒表", command =mode2)
menubar.add_command(label ="倒计时",command =mode3)
menubar.add_command(label ="退出",command =mode4)
window.config(menu = menubar)
window.mainloop()
