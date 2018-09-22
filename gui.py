# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 15:14:47 2017

@author: Bhavya
"""
import os
from tkinter import *
root=Tk()
root.title("LP-GUI")

header=Label(root,text="Enter the required values.\nThen press the button 'import variables'.\nThen run any model.")
header.grid(row=0,columnspan=2)

label1 =Label(root,text="Enter Nmax:")
label2 =Label(root,text="Enter D1:")
label3 =Label(root,text="Enter D2:")
entry1=Entry(root)
entry2=Entry(root)
entry3=Entry(root)

label1.grid(row=1,column=0)
label2.grid(row=2,column=0)
label3.grid(row=3,column=0)
entry1.grid(row=1,column=1)
entry2.grid(row=2,column=1)
entry3.grid(row=3,column=1)

button1=Button(root,text="Run model 1")
button2=Button(root,text="Run model 2")
button4=Button(root,text="Run model 4")
button8=Button(root,text="Run model 8")
button=Button(root,text="import variables")
button1.grid(row=5,columnspan=2)
button2.grid(row=6,columnspan=2)
button4.grid(row=7,columnspan=2)
button8.grid(row=8,columnspan=2)
button.grid(row=4,columnspan=2)

def model1(event):
    os.system("python model1.py")
def model2(event):
    os.system("python model2.py")
def model4(event):
    os.system("python model4.py")
def model8(event):
    os.system("python model8.py")
def var(event):
    global Nmax
    print("hoya kuch")
    Nmax=int(entry1.get())
    global D1
    D1=int(entry2.get())
    global D2
    D2=int(entry3.get())
    f=open("Parameters.txt",'w')
    f.truncate()
    f.write(str(Nmax))
    f.write("\n")
    f.write(str(D1))
    f.write("\n")
    f.write(str(D2))
    f.close()

button1.bind("<Button-1>", model1)
button2.bind("<Button-1>", model2)
button4.bind("<Button-1>", model4)
button8.bind("<Button-1>", model8)
button.bind("<Button-1>",var)

root.mainloop()



