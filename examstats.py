import numpy as np
import pandas as pd
import sys
import tkinter as tk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

FONT_NAME = "Times"

def order(a):
    return float(a["Marks"])


purpose = sys.argv[1]
def examstats(test):  

    # Create a frame with a specific width and height
    area_frame = tk.Frame(window, width=1500, height=800, bg="white")
    area_frame.grid(column=0,row=1,columnspan=96,rowspan=120) 

    #will contain stat details
    stat_of_all={}
    stat_of_present={}
    
    #file read and required data store in variable
    data_of_present_students=pd.read_csv(f"{test}.csv")
    marks_of_present = data_of_present_students["Marks"]

    #data stored in form of  dictionary
    data_dict = data_of_present_students.to_dict(orient="records")

    ##data sorted on the basis of marks
    data_dict = sorted(data_dict, key=lambda a: order(a))

    data = pd.read_csv('main.csv')
    marks = data[f"{test}"]

    total_num_of_students = len(marks)
    num_of_students_present=len(marks_of_present)
    num_of_students_absent = total_num_of_students-num_of_students_present


    marks.replace('a', 0, inplace=True)
    marks = pd.to_numeric(marks)

    ######################################################################################
    ######################################################################################
    ##stats value are calculated 

    #this contains stats considering all student also those who were absent
    stat_of_all["Lowest Marks"] = marks.min()
    stat_of_all["Highest Marks"] = marks.max()
    stat_of_all["Mean "] = round(marks.mean(),2)
    stat_of_all["Median"] = marks.median()
    stat_of_all["Standard deviation"] = round(marks.std(),2)

    #this contains stats considering only present student
    stat_of_present["Lowest Marks"] = marks_of_present.min()
    stat_of_present["Highest Marks"] = marks_of_present.max()
    stat_of_present["Mean "] = round(marks_of_present.mean(),2)
    stat_of_present["Median"] = marks_of_present.median()
    stat_of_present["Standard deviation"] = round(marks_of_present.std(),2)

    ######################################################################################
    ######################################################################################
    # the figure that will contain the plot
    fig = Figure(figsize = (10,7), dpi = 100)

    #suptitle given
    fig.suptitle(f"Stats of exam : {test}",fontdict={'family': 'serif','color':'red','size':18})
    
    #histogram 
    plot1=fig.add_subplot(211)
    plot1.hist(marks,bins=20,color="#484848")
    plot1.grid(True)
    plot1.set_title("Frequency Distribution of Marks",fontdict={'family': 'serif', 'size': 14,'color':'#C80000'})
    plot1.set_xlabel("Marks",fontdict={'family': 'serif', 'size': 14,'color':'#6600CC'})
    plot1.set_ylabel("Frequency",fontdict={'family': 'serif', 'size': 14,'color':'#6600CC'})


    #PIE chart
    plot2=fig.add_subplot(212)
    y=[num_of_students_present,num_of_students_absent]
    plot2.pie(y, labels = ["Present","Absent"],colors=["green","red"],autopct='%1.1f%%', textprops={'fontsize': 10})

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, master = window)   
    canvas.draw() 
  
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().grid(column=0,row=1,rowspan=120,columnspan=90)


    ######################################################################################
    ######################################################################################
    num_of_students_present_label = tk.Label(text="Number of student present in exam :",font=(FONT_NAME,15,"bold"),background="white",fg="green")
    num_of_students_present_label.grid(column=91,row=2)

    present=tk.Label(text=f"{num_of_students_present} ",font=(FONT_NAME,15),background="white",fg="green")
    present.grid(column=92,row=2)

    num_of_students_absent_label = tk.Label(text="Number of student absent in exam :",font=(FONT_NAME,15,"bold"),background="white",fg="red")
    num_of_students_absent_label.grid(column=91,row=3)

    absent=tk.Label(text=f"{num_of_students_absent}",font=(FONT_NAME,15,"bold"),background="white",fg="red")
    absent.grid(column=92,row=3)

    total_label = tk.Label(text="Total number of student in exam :",font=(FONT_NAME,15,"bold"),background="white")
    total_label.grid(column=91,row=4)

    total = tk.Label(text=f"{total_num_of_students}",font=(FONT_NAME,15,"bold"),background="white")
    total.grid(column=92,row=4)

    ######################################################################################
    ######################################################################################

    Heading = tk.Label(text="--------------------------------------------------\n List of Toppers\n --------------------------------------------------",font=(FONT_NAME,15,"bold"),background="white",fg="#0E46A3")
    Heading.grid(columnspan=2,column=91,row=10)
    if total_num_of_students-num_of_students_absent >=5:
        toppers = data_dict[:-6:-1]
    else:
        toppers = data_dict[:-(total_num_of_students-num_of_students_absent)-1:-1]
    i=14
    for x in toppers:
        name=tk.Label(text=f"{i-13}) {x['Name']}",font=(FONT_NAME,15,"bold"),background="white")
        name.grid(column=91,row=i)
        mark = tk.Label(text=x[f"Marks"], font=(FONT_NAME, 15, "bold"), background="white")
        mark.grid(column=92, row=i)

        i+=1
    i+=10

    ######################################################################################
    ######################################################################################
    i=29
    Heading = tk.Label(text="--------------------------------------------------\n Stats of exam considering all students\n--------------------------------------------------",font=(FONT_NAME,15,"bold"),background="white",fg="#0E46A3")
    Heading.grid(columnspan=2,column=91,row=i)
    i+=4
    for x in stat_of_all:
        quantity = tk.Label(text=f"{x}", font=(FONT_NAME, 15, "bold"), background="white")
        quantity.grid(column=91, row=i)
        value = tk.Label(text=f"{stat_of_all[x]}", font=(FONT_NAME, 15, "bold"), background="white")
        value.grid(column=92, row=i)
        i+=1

    i+=10

    ######################################################################################
    ######################################################################################

    Heading = tk.Label(text="--------------------------------------------------\n Stats of only present students\n--------------------------------------------------",font=(FONT_NAME,15,"bold"),background="white",fg="#0E46A3")
    Heading.grid(columnspan=2,column=91,row=i)
    i+=4
    for x in stat_of_present:
        quantity = tk.Label(text=f"{x}", font=(FONT_NAME, 15, "bold"), background="white")
        quantity.grid(column=91, row=i)
        value = tk.Label(text=f"{stat_of_present[x]}", font=(FONT_NAME, 15, "bold"), background="white")
        value.grid(column=92, row=i)
        i+=1

    




list_of_exams=sys.argv[1:]

window = tk.Tk()
window.config(background="white")


######################################################################################
######################################################################################

j=0
for x in list_of_exams:
    # Create a button with custom style
    button = tk.Button(master=window,  
                    command=lambda exam_name=x: examstats(exam_name),
                    text=f"{x}",
                    font=("serif", 8),  # Set font
                    bg="#007BFF",  # Set background color
                    fg="white",  # Set text color
                    relief=tk.RAISED,  # Set relief style
                    borderwidth=2,  # Set border width
                    highlightbackground="#007BFF",  # Set border color when focused
                    highlightcolor="#007BFF",  # Set border color when focused
                    width=10,  # Set width
                    height=2)  # Set height

    # Place the button in the main window
    button.grid(column=j, row=0, padx=5, pady=5)  # Add padding around the button
    j+=1

tk.mainloop()