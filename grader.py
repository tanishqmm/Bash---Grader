import numpy as np
import pandas as pd
import sys
import tkinter as tk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

def grader_plot(exam_name):
    
    ##Read dsta from that exam.csv
    data=pd.read_csv(f'{exam_name}.csv')

    grades=[]##list wich will store grades of students
    marks=np.array(data["Marks"].values) #takes marks column as an array
    mean=np.mean(marks) #calculate mean of all marks
    std=np.std(marks) #calculate std of all marks

    ##this criteria of grading is followed in many institutes (Came to know by searching on Internet)
    a_plus_1_5_sd = mean + 1.5 * std
    a_plus_1_sd = mean + 1.0 * std
    a_plus_0_5_sd = mean + 0.5 * std
    a_minus_0_5_sd = mean - 0.5 * std
    a_minus_1_sd = mean - 1.0 * std
    a_minus_1_5_sd = mean - 1.5 * std
    
    # Assign grades based on marks
    for x in marks:
        if x >= a_plus_1_5_sd:
            grades.append(10)
        elif x >= a_plus_1_sd:
            grades.append(9)
        elif x >= a_plus_0_5_sd:
            grades.append(8)
        elif x >= mean:
            grades.append(7)
        elif x > a_minus_0_5_sd:
            grades.append(6)
        elif x > a_minus_1_sd:
            grades.append(5)
        elif x > a_minus_1_5_sd:
            grades.append(4)
        else:
            grades.append(3)
        
    ##list with Rollnumber,name,grades 
    graded_marks=list(zip(data["Roll_Number"].values,data["Name"].values,grades))
    with open("grades.txt",mode="w") as f:
        f.write(f"Exan name :{exam_name}\n \nRoll,Name,grade\n------------------ \n")
    with open("grades.txt",mode="a") as f:    
        for roll,name,grade in graded_marks:
            f.write(f"{roll},{name},{grade}\n")


    num=[]##store count of how many people got a particular grade
    for i in range(3,11):
        num.append(grades.count(i))

    # the figure that will contain the plot
    fig = Figure(figsize = (10,5), dpi = 100)

    fig.suptitle(f"Frequency of getting a particular Grade in {exam_name}",fontdict={'family': 'serif','color':'red'})


    ##PIE chart
    plot1 = fig.add_subplot(121)
    mylabels = range(3,11)
    plot1.pie(num, labels = mylabels, autopct='%1.1f%%')
    plot1.legend()

    ##Line graph
    plot2 = fig.add_subplot(122)
    plot2.plot(["10","9","8","7","6","5","4","3"], num[::-1],marker="o",linestyle="--")
    plot2.set_xlabel('Grades',fontdict={'family': 'serif', 'size': 14,'color':'blue'})
    plot2.set_ylabel('Frequency',fontdict={'family': 'serif', 'size': 14,'color':'blue'})
    plot2.grid(True)

    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, master = window)   
    canvas.draw() 
  
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().grid(column=0,row=1,columnspan=100)


list_of_exams=sys.argv[1:]

##initialise the main tk window
window = tk.Tk()
window.config(padx=20, pady=20, background="#F5F5F5")
window.title("Grades alloted")

i=0
for x in list_of_exams:
    # Create a button with custom style
    button = tk.Button(master=window,  
                    command=lambda exam_name=x: grader_plot(exam_name),
                    text=f"{x}",
                    font=("serif", 13),  # Set font
                    bg="#007BFF",  # Set background color
                    fg="white",  # Set text color
                    relief=tk.RAISED,  # Set relief style
                    borderwidth=2,  # Set border width
                    highlightbackground="#007BFF",  # Set border color when focused
                    highlightcolor="#007BFF",  # Set border color when focused
                    width=10,  # Set width
                    height=2)  # Set height

    # Place the button in the main window
    button.grid(column=i, row=0, padx=5, pady=5)  # Add padding around the button
    i+=1


tk.mainloop()




