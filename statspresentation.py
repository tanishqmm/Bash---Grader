import sys
import pandas as pd
import tkinter as tk

FONT_NAME = "Times"

def order(a):
    return float(a["Marks"])


purpose = sys.argv[1]
if purpose.lower()=="student":

    Roll=sys.argv[2]
    data = pd.read_csv('main.csv')
    sub_data=data[data.Roll_Number == Roll.lower()]
    name_of_student=sub_data["Name"].values[0]
    with open("main.csv") as f:
        header=f.readline().strip()
    header=header.split(",")[2:] 
    Exams=[]
    Marks = {}
    absent=[]
    Rank={}
    for x in header:
        m=sub_data[f"{x}"].values[0]
        if(f"{m}"!="a"):
            Exams.append(x)
            Marks[x]=float(m)
            allstudentmarks = data[f"{x}"]
            allstudentmarks.replace('a', 0, inplace=True)
            allstudentmarks = pd.to_numeric(allstudentmarks)
            Rank[x]=len(allstudentmarks[allstudentmarks>float(m)])+1     
        else:
            absent.append(x)
            Marks[x]=0
        
    ######################################################################################
    ######################################################################################

    window = tk.Tk()
    window.config(padx=40, pady=40, background="#F5F5F5")

    ######################################################################################
    ######################################################################################

    canvas = tk.Canvas(width=640, height=480)
    mad = tk.PhotoImage(file="./.images/roll.png")
    canvas.create_image(320, 240, image=mad)
    canvas.grid(column=0,row=0,rowspan=44)
    canvas = tk.Canvas(width=640, height=480)
    comparison = tk.PhotoImage(file="./.images/comparison.png")
    canvas.create_image(320, 240, image=comparison)
    canvas.grid(column=0, row=45, rowspan=40)

    ######################################################################################
    ######################################################################################

    Name =tk.Label(text="Name :", font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="Red")
    Name.grid(column=1, row=5)
    Name = tk.Label(text=f"{name_of_student}", font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="red")
    Name.grid(column=2, row=5)

    Rollnum = tk.Label(text="Roll number :", font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="Red")
    Rollnum.grid(column=1, row=7)
    Rollnum = tk.Label(text=f"{Roll}", font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="red")
    Rollnum.grid(column=2, row=7)

    ######################################################################################
    ######################################################################################
    i=10
    if len(Rank)!=0:
        Heading = tk.Label(text="--------------------------------------------------\n Rank secured in Exams\n--------------------------------------------------",font=(FONT_NAME, 15, "bold"), background="#F5F5F5", fg="#0E46A3")
        Heading.grid(columnspan=2, column=1, row=i)
        i+=2
        Heading = tk.Label(text="Exam",font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="#0E46A3")
        Heading.grid( column=1, row=i)
        Heading = tk.Label(text="Rank", font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="#0E46A3")
        Heading.grid(column=2, row=i)
        i+=2
        for x in Rank:
            name = tk.Label(text=f"{x}", font=(FONT_NAME, 15, "bold"),background="#F5F5F5")
            name.grid(column=1, row=i)

            rank = tk.Label(text=f"{Rank[x]}", font=(FONT_NAME, 15, "bold"), background="#F5F5F5")
            rank.grid(column=2, row=i)
            i+=1
        i+=15
    ######################################################################################
    ######################################################################################
    if len(absent)!=0:
        Heading = tk.Label(text="--------------------------------------------------\n Exams for which he/she was absent\n--------------------------------------------------",font=(FONT_NAME, 15, "bold"), background="#F5F5F5", fg="#0E46A3")
        Heading.grid(columnspan=2, column=1, row=i)
        i+=1
        for x in absent:
            name = tk.Label(text=f"{x}", font=(FONT_NAME, 15, "bold"), background="#F5F5F5")
            name.grid(column=1, row=i,columnspan=2)
            i+=1
        i+=15

    ######################################################################################
    ######################################################################################

    if len(Marks)!=0:
        Heading = tk.Label(text="--------------------------------------------------\n Marks Scored\n--------------------------------------------------",font=(FONT_NAME, 15, "bold"), background="#F5F5F5", fg="#0E46A3")
        Heading.grid(columnspan=2, column=1, row=i)
        i+=2
        Heading = tk.Label(text="Exam",font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="#0E46A3")
        Heading.grid( column=1, row=i)
        Heading = tk.Label(text="Marks", font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="#0E46A3")
        Heading.grid(column=2, row=i)
        i+=2
        for x in Marks:
            name = tk.Label(text=f"{x}", font=(FONT_NAME, 15, "bold"),background="#F5F5F5")
            name.grid(column=1, row=i)

            rank = tk.Label(text=f"{Marks[x]}", font=(FONT_NAME, 15, "bold"), background="#F5F5F5")
            rank.grid(column=2, row=i)
            i+=1
        i+=5

    tk.mainloop()



######################################################################################
######################################################################################
######################################################################################
######################################################################################

elif purpose.lower()=="compare":
    s1=sys.argv[2]
    s2=sys.argv[3]

    data=pd.read_csv('main.csv')
    s1_data=data[data.Roll_Number == s1.lower()]
    s2_data=data[data.Roll_Number == s2.lower()]

    with open("main.csv") as f:
        header=f.readline().strip()
    header=header.split(",")[2:]
    
    s1_name=s1_data.Name.values[0]
    s1_status={}
    s1_marks=[]

    s2_status={}
    s2_marks=[]
    s2_name=s2_data.Name.values[0]

    for x in header:
        m=s1_data[f"{x}"].values[0]
        if(f"{m}"!="a"):
            s1_status[x]="Present"
            s1_marks.append(float(m))
        else:
            s1_status[x]="Absent"
            s1_marks.append(0)

        m=s2_data[f"{x}"].values[0]
        if(f"{m}"!="a"):
            s2_status[x]="Present"
            s2_marks.append(float(m))
        else:
            s2_status[x]="Absent"
            s2_marks.append(0)

        
    ######################################################################################
    ######################################################################################

    window = tk.Tk()
    window.config(padx=40, pady=40, background="#F5F5F5")

    ######################################################################################
    ######################################################################################

    
    Name = tk.Label(text=f"Name of s1 : {s1_name} ({s1})", font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="red")
    Name.grid(column=0, row=0,columnspan=6)
    
    Name = tk.Label(text=f"Name of s2 : {s2_name} ({s2})", font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="red")
    Name.grid(column=0, row=1,columnspan=6)
    
    ######################################################################################
    ######################################################################################

    canvas = tk.Canvas(width=640, height=480)
    comp = tk.PhotoImage(file="./.images/comparison_s1_s2.png")
    canvas.create_image(320, 240, image=comp)
    canvas.grid(column=0,row=3,rowspan=44,padx=40)

    ######################################################################################
    ######################################################################################

    i=6
    Heading = tk.Label(text="------------------------------------------------------------------\n Marks Scored AND status of exam \n------------------------------------------------------------------",font=(FONT_NAME, 15, "bold"), background="#F5F5F5", fg="#0E46A3")
    Heading.grid(columnspan=4, column=2, row=i)
    i+=2
    Heading = tk.Label(text=f"{s1}",font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="#0E46A3")
    Heading.grid( column=2, row=i,columnspan=2)
    Heading = tk.Label(text=f"{s2}", font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="#0E46A3")
    Heading.grid(column=4, row=i,columnspan=2)
    i+=2
    Heading = tk.Label(text=f"Marks",font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="#0E46A3")
    Heading.grid( column=2, row=i)
    Heading = tk.Label(text=f"Status", font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="#0E46A3")
    Heading.grid(column=3, row=i)
    Heading = tk.Label(text=f"Marks",font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="#0E46A3")
    Heading.grid( column=4, row=i)
    Heading = tk.Label(text=f"Status", font=(FONT_NAME, 20, "bold"), background="#F5F5F5", fg="#0E46A3")
    Heading.grid(column=5, row=i)
    i+=2
    for x in range(len(header)):
        name = tk.Label(text=f"{header[x]} ", font=(FONT_NAME, 20, "bold"),background="#F5F5F5",fg="#9900CC")
        name.grid(column=1, row=i)
        marks = tk.Label(text=f"{s1_marks[x]}", font=(FONT_NAME, 15, "bold"), background="#F5F5F5")
        marks.grid(column=2, row=i)
        status = tk.Label(text=f"{s1_status[header[x]]}", font=(FONT_NAME, 15, "bold"), background="#F5F5F5")
        status.grid(column=3, row=i)

        marks = tk.Label(text=f"{s2_marks[x]}", font=(FONT_NAME, 15, "bold"), background="#F5F5F5")
        marks.grid(column=4, row=i)
        status = tk.Label(text=f"{s2_status[header[x]]}", font=(FONT_NAME, 15, "bold"), background="#F5F5F5")
        status.grid(column=5, row=i)
    
        i+=1
    i+=15

    ######################################################################################
    ######################################################################################


    tk.mainloop()