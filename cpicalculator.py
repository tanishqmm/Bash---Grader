from tkinter import *

credit_list = []
grades_list = []
i = 2
FONT_NAME="Times"
BACKGROUNDCOLOR="#F9E4BC"


##This function contains the algorithm of calculating cpi
def Calculate_CPI():
    sum_of_credit=0
    score=0
    for i in range(len(grades_list)):
        sum_of_credit+=float(credit_list[i].get())
        score+=float(credit_list[i].get())*float(grades_list[i].get())/10
   
    heading = Label(root, text=f"{round((score/sum_of_credit)*10,2)}", font=(FONT_NAME, 20, "bold"),fg="red",background=BACKGROUNDCOLOR)
    heading.grid(column=0, row=13,columnspan=6)

##if we have toh add subject then (max subject which we can add is 10)
def add_subject():
    global i
    if i==12:
        return
    
    subject_label = Label(root, text="Course Name", font=(FONT_NAME, 15, "bold"),background=BACKGROUNDCOLOR,fg="green")
    subject_label.grid(column=0, row=i, padx=(10, 5),pady=(5,10))  
    subject_name = Entry(root)
    subject_name.grid(column=1, row=i, padx=(0, 10),pady=(5,10))  
    
    grade_label = Label(root, text="Grade", font=(FONT_NAME, 15, "bold"),background=BACKGROUNDCOLOR,fg="green")
    grade_label.grid(column=2, row=i, padx=(10, 5),pady=(5,10)) 
    grade = Entry(root)
    grade.grid(column=3, row=i, padx=(0, 10),pady=(5,10)) 
    grades_list.append(grade)

    credit_of_exam_label = Label(root, text="Credit", font=(FONT_NAME, 15, "bold"),background=BACKGROUNDCOLOR,fg="green")
    credit_of_exam_label.grid(column=4, row=i, padx=(10, 5),pady=(5,10)) 
    credit_of_exam = Entry(root)
    credit_of_exam.grid(column=5, row=i, padx=(0, 10),pady=(5,10))  
    credit_list.append(credit_of_exam)

    i += 1

##initialize root window
root = Tk()
root.config(padx=30,pady=30,background=BACKGROUNDCOLOR)

heading = Label(root, text="CPI Calculator", font=(FONT_NAME, 20, "bold"),fg="red",background=BACKGROUNDCOLOR)
heading.grid(column=0, row=0,columnspan=6)

button = Button(root, text="Add Course", command=add_subject,fg="#0E46A3",background="#9AC8CD",font=(FONT_NAME, 15, "bold"))
button.grid(column=0, row=1,columnspan=6,pady=(5,10))

button = Button(root, text="Calculate cpi", command=Calculate_CPI,fg="#0E46A3",background="#9AC8CD",font=(FONT_NAME, 15, "bold"))
button.grid(column=0, row=12,columnspan=6,pady=(5,10))


mainloop()
