# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 09:11:41 2017

@author: Administrator
"""
from tkinter import*
root=Tk()
root.title("something")
root.geometry('2000x1000')
root.resizable(width=True,height=True)
Label(root,bg='red',width=10,height=5,text='带搜').pack()
frm=Frame(root)
frame_l=Frame(frm)
frame_l.pack(side=LEFT)
Label(frame_l,text='左护法',font=('Arial', 15)).pack(side=TOP)
Label(frame_l,text='左军师',font=('Arial', 15)).pack(side=TOP)   
root.mainloop()