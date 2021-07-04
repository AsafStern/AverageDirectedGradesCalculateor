# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 10:49:24 2020

@author: Asaf Stern
"""

import tkinter as tk
from tkinter import filedialog , Text, ttk




class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        s = ttk.Style()
        s.configure('TFrame',backround = 'white')
        canvas = tk.Canvas(container,height = 200, width = 300)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, style='TFrame')

        self.scrollable_frame.bind(\
            "<Configure>",\
            lambda e: canvas.configure(\
                scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", expand=True)
        scrollbar.pack(side="right", fill="y")
        


def GradesOption(listOfCourses, listOfPluses, neededPlus, dictionary, differPara, OptionsFlag, file, tupleVal=()):
    if neededPlus <= sum(listOfPluses):
        if not OptionsFlag[0]:
            file.write("Your Options Are - \n\n")
            OptionsFlag[0]=True
        file.write(dictionary[tupleVal])
        print(dictionary[tupleVal])
        return
    for i in range(len(listOfPluses)):
        newList = listOfPluses[:]
        newList[i] += differPara*listOfCourses[i][2]
        if listOfCourses[i][1]+(newList[i]/listOfCourses[i][2]) <= 100:
            printedSTR = ""
            tupleVal = []
            for i in range(len(listOfCourses)):
                tupleVal.append(listOfCourses[i][0] + str(int(newList[i]/listOfCourses[i][2])))
                printedSTR += str(listOfCourses[i][0]) + " +" + str(int(newList[i]/listOfCourses[i][2]))\
                + "  " + "final: "+str(int((listOfCourses[i][1]+(newList[i]/listOfCourses[i][2]))))+"\n"
            tupleVal = tuple(tupleVal)
            if tupleVal not in dictionary:
                dictionary[tupleVal] = printedSTR+"\n"
                GradesOption(listOfCourses, newList, neededPlus, dictionary, differPara,OptionsFlag, file, tupleVal)



def WhatAreMyOptions(wantedGrade, totalPoints, currentGrade, listOfCourses, differPara, file):
    print("\nStarting Point- \nTotal Credit Points: "+str(totalPoints)+"\n Current Average: "+str(currentGrade)\
      +"\n\nYour Options Are - \n")
    pointsCounter = 0
    listOfPluses = []
    gradesCounter = 0
    for val in listOfCourses:
        pointsCounter += val[2]
        gradesCounter += val[1]
        listOfPluses.append(0)
    neededPlus = totalPoints*(wantedGrade - currentGrade)
    if neededPlus <= sum(listOfPluses):
        file.write("\n Needed average achicved! \n\n")
    else:
        if len(listOfCourses)<1:
            file.write("\n  No availible options\n  Chose a course to improve your grade.")
        else:
            Optionsflag=[False]
            GradesOption(listOfCourses, listOfPluses, neededPlus, {():""}, differPara, Optionsflag ,file)
            if not Optionsflag[0]:
                file.write("\n  Unable to achive needed average\n  with chosen courses.\n\n")
    
    
def gettingStats(listOfCourses):
    currentAverage = 0
    totalPoints = 0
    for var in listOfCourses:
        currentAverage += var[1]*var[2]
        totalPoints += var[2]
    currentAverage = currentAverage/totalPoints
    return currentAverage, totalPoints


root= tk.Tk(className= " Average Directed Grades Calculator")
master = tk.Canvas(root,height = 500, width = 1000, background="lightblue")
master.pack(fill = "both",expand = True)
canvas = tk.Canvas(master,height = 300, width = 800, background="lightblue")
canvas.pack(side="left", anchor="n")
scoresOut= tk.Frame(master,height = 50, background="lightblue")
scoresOut.pack(anchor="nw")
output = ScrollableFrame(master)


frame = tk.Frame(canvas, background="lightblue")
frame.pack(side = "left", anchor = "n",pady=40)

tmpL = ttk.Label(output.scrollable_frame,text="")
tmpL.pack()

can = tk.Frame(canvas,height = 20 , width = 20, background="lightblue")
can.pack(side= "bottom" ,anchor="s")


checkbox = tk.Frame(canvas, bd=0.1, background="lightblue")
checkbox.pack(side="left" , anchor = "n")

labels = tk.Frame(canvas, background="lightblue")
labels.pack(side="left", anchor = "n")

labels2 = tk.Frame(canvas, background="lightblue")
labels2.pack(side="left", anchor = "n")

labels3 = tk.Frame(canvas, background="lightblue")
labels3.pack(side="left", anchor = "n")

courses = tk.Frame(canvas, background="lightblue")
courses.pack(side = "left", anchor = "n")

C = tk.Label(checkbox,height=2, text="Improve  ", background="lightblue")
C.pack(anchor = "nw")
L = tk.Label(labels,height=2, text="     Course", background="lightblue")
L.pack(anchor = "nw")
L2 = tk.Label(labels2,height=2, text="  Grade  ", background="lightblue")
L2.pack(anchor = "nw")
L3 = tk.Label(labels3,height=2, text="     Credit  ", background="lightblue")
L3.pack(anchor = "nw")
L = tk.Label(courses,height=2, text="", background="lightblue")
L.pack(anchor = "w")



listOC = {}
checkedList = {}

def add_remove(relTupple):
    if relTupple not in checkedList:
        checkedList[relTupple]=None
    else:
        checkedList.pop(relTupple)
    RunFlow()

def remove(c1,d1,l,l2,l3,data):
    if data in listOC:
        listOC.pop(data)
    if data in checkedList:
        checkedList.pop(data)
    c1.destroy()
    d1.destroy()
    name = l["text"][:-2]
    grade = l2["text"][1:]
    points = l3["text"][3:]
    l.destroy()
    l2.destroy()
    l3.destroy()
    e1.delete(0, 'end')
    e2.delete(0, 'end')
    e3.delete(0, 'end')
    e1.insert(0,name)
    e2.insert(0,grade)
    e3.insert(0,points)
    RunFlow()
    

def Creator():
    try:
        relTupple = (str(e1.get()),int(e2.get()),int(e3.get()))
    except:
        relTupple = (str(e1.get()),int(e2.get()),float(e3.get()))
    course_print = "" + e1.get()+"  "
    course_print2=" "+e2.get()
    course_print3="   "+ e3.get()
    if relTupple in listOC:
        return
    listOC[relTupple]=None
    var = tk.IntVar(0)
    C1 = tk.Checkbutton(checkbox,height=2, command = lambda: add_remove(relTupple) ,\
                 variable = var, onvalue = 1, offvalue = 0, \
                 width = 0, background="lightblue")
    L = tk.Label(labels,height=2, text=course_print, font=("Ariel", 11), background="lightblue")
    L.pack(anchor = "w")
    L2 = tk.Label(labels2,height=2, text=course_print2, font=("Ariel", 11), background="lightblue")
    L2.pack(anchor = "center")
    L3 = tk.Label(labels3,height=2, text=course_print3, font=("Ariel", 11), background="lightblue")
    L3.pack(anchor = "center")
    D1 = tk.Button(courses,height=1, text="remove",command = lambda: remove(C1,D1,L,L2,L3,relTupple))
    C1.pack(anchor="center")
    D1.pack(pady=7)
    RunFlow()
    
def Defult(relTupple):
    course_print = "" + relTupple[0]+"  "
    course_print2=" "+str(relTupple[1])
    course_print3="   "+str(relTupple[2])
    listOC[relTupple]=None
    var = tk.IntVar(0)
    C1 = tk.Checkbutton(checkbox,height=2, command = lambda: add_remove(relTupple) ,\
                 variable = var, onvalue = 1, offvalue = 0, \
                 width = 0, background="lightblue")
    L = tk.Label(labels,height=2, text=course_print, font=("Ariel", 11), background="lightblue")
    L.pack(anchor = "w")
    L2 = tk.Label(labels2,height=2, text=course_print2, font=("Ariel", 11), background="lightblue")
    L2.pack(anchor = "center")
    L3 = tk.Label(labels3,height=2, text=course_print3, font=("Ariel", 11), background="lightblue")
    L3.pack(anchor = "center")
    D1 = tk.Button(courses,height=1, text="remove",command = lambda: remove(C1,D1,L,L2,L3,relTupple))
    C1.pack(anchor="center")
    D1.pack(pady=7)
    
    
def RunFlow():
    if len(scoresOut.pack_slaves()) > 0:
        scoresOut.pack_slaves()[0].destroy()
    LOC = list(listOC.keys())
    AvTp = gettingStats(LOC)
    totalCreditPoints = AvTp[1]  #of all courses
    currentAverage = AvTp[0]   #of all courses
    textie="\n\n     Average:              "+\
    '{:.6}'.format(str(currentAverage))+"\n\n     Credit Points:       "+str(totalCreditPoints)
    ttk.Label(scoresOut, text=textie, font=("Ariel",13), background="lightblue").pack(anchor="w")
    for label in frame.grid_slaves():
        if int(label.grid_info()["row"]) > 6 and int(label.grid_info()["column"]) > 0:
            label.grid_forget()
    LORC=list(checkedList.keys())
    if len(checkedList)>0:
        tk.Label(frame, text="results sort-", background="lightblue").grid(row=8, column=1)
        for i in range(len(LORC)):
            tk.Label(frame, text=LORC[i][0], background="lightblue").grid(row=i+9, column=1)
        


def difPara(num):
    if len(checkedList) < 4:
        return  1
    if len(checkedList)< 5:
        return  3
    if len(checkedList) < 7:
        return  5
    return  10

def Runner(neededGrade):
    for i in range(2):
        if len(output.scrollable_frame.pack_slaves()) > 0:
            output.scrollable_frame.pack_slaves()[0].destroy()
        if len(scoresOut.pack_slaves()) > 0:
            scoresOut.pack_slaves()[0].destroy()
    print(list(listOC.keys()))
    file = open("outputText.txt","w")
    AvTp = gettingStats(list(listOC.keys()))
    differPara = difPara(len(checkedList))
    totalCreditPoints = AvTp[1]  #of all courses
    currentAverage = AvTp[0]   #of all courses
    textie="\n\n     Average:              "+\
    '{:.6}'.format(str(currentAverage))+"\n\n     Credit Points:       "+str(totalCreditPoints)
    ttk.Label(scoresOut, text=textie, font=("Ariel",13), background="lightblue").pack(anchor="w")
    WhatAreMyOptions(      neededGrade         \
                    ,   totalCreditPoints      \
                    ,    currentAverage        \
                    , list(checkedList.keys()) \
                    ,      differPara          \
                    ,         file             )
    
    file.close()
    with open("outputText.txt", 'r') as f:
        txt = f.read()
    ttk.Label(output.scrollable_frame, text=txt).pack(padx = 40)
    output.pack(side = "right")
    

def setDefult():
    file = open("Defult.txt","w")
    for tup in listOC:
        file.write(tup[0] +"~"+ str(tup[1]) +"~"+ str(tup[2]) + "\n")
    file.close()
    
def OpenDefult():
    try:
        file = open("Defult.txt","r")
        nextList = []
        for line in file.read().split("\n"):
            nextTup = line.split("~")
            if len(nextTup) > 2:
                try:
                    nextTup[1] = int(nextTup[1])
                except:
                    nextTup[1] = float(nextTup[1])
                try:
                    nextTup[2] = int(nextTup[2])
                except:
                    nextTup[2] = float(nextTup[2])
                nextList.append(tuple(nextTup))
        print(nextList)
        file.close()
        return nextList
    except:
        tmp = open("Defult.txt","w")
        tmp.close()
        return OpenDefult()
    
    
c1 = tk.Label(frame, text="Course Name", background="lightblue")
c1.grid(row=0, column=0)
e1 = tk.Entry(frame)
e1.grid(row=0, column=1)
e1.insert(0,"")
c2 = tk.Label(frame, text="Course Grade" , background="lightblue")
c2.grid(row=1, column=0)
e2 = tk.Entry(frame)
e2.grid(row=1, column=1)
e2.insert(1,"")
c3 = tk.Label(frame, text="Credit Points", background="lightblue")
c3.grid(row=2, column=0)
e3 = tk.Entry(frame)
e3.grid(row=2, column=1)
e3.insert(2,"")


addCourse = tk.Button(frame, text="add course", command = Creator)
addCourse.grid(row=3, column=1)

setD = tk.Frame(can)
setD.pack(side = "right",anchor = "center")

setD = tk.Button(can, text="Set above courses as defult when re-open", command = setDefult)
setD.pack(side = "right",anchor = "center")

c4 = tk.Label(frame, text="Average Needed", background="lightblue")
c4.grid(row=5, column=0)
e4 = tk.Entry(frame, width=2)
e4.grid(row=6, column=0)
e4.insert(3,"90")

run = tk.Button(frame, text="Check Options", command = lambda: Runner(float(e4.get())))
run.grid(row=7, column=0)


#startLst=[(    "Programming Intro"      , 91  , 5   )\
#         ,(    "Linear Algebra"         , 87  , 4.5 )\
#         ,(    "Calculus 1"             , 88  , 5   )\
#         ,(    "Calculus 2"             , 66  , 5   )\
#         ,(    "Data Structures"        , 88  , 5   )\
#         ,(    "Physics"                , 100 , 5   )\
#         ,(    "Logics"                 , 84  , 5   )\
#         ,(    "OOP"                    , 75  , 3   )]


startLst = OpenDefult()
if len(startLst) == 0:
    startLst = [('Example Course',84,3)]


for var in startLst:
    Defult(var)
RunFlow()



root.mainloop()