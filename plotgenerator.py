import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
purpose=sys.argv[1]


if purpose =="student":
    Roll=sys.argv[2]
    data = pd.read_csv('main.csv')
    sub_data=data[data.Roll_Number == Roll.lower()]

    with open("main.csv") as f:
        header=f.readline().strip()
    header=header.split(",")[2:] 
    Exams=[]
    Marks = []

    
    avg_marks_of_all_student=[]
    
    for x in header:
        m=sub_data[f"{x}"].values[0]
        if(f"{m}"=="a"):
            Marks.append(0)
        else:
            Marks.append(float(m))
        Exams.append(x)
        
        allstudentmarks = data[f"{x}"]
        allstudentmarks.replace('a', 0, inplace=True)
        allstudentmarks = pd.to_numeric(allstudentmarks)
        avg_marks_of_all_student.append(allstudentmarks.mean())

    
    plt.plot(Exams, Marks,marker="o",linestyle="--")
    plt.xlabel('Exams',fontdict={'family': 'serif', 'size': 14,'color':'blue'})
    plt.ylabel('Marks',fontdict={'family': 'serif', 'size': 14,'color':'blue'})
    plt.title('Distribution of marks in attempted exams',fontdict={'family': 'serif', 'size': 17})
    plt.grid(True)
    plt.savefig("./.images/roll.png")
    plt.clf()
    ###############################################################
    # Define the width of the bars
    bar_width = 0.35

    # Define the x locations for the groups
    index = np.arange(len(Exams))

    # Create the figure and axes objects
    fig, ax = plt.subplots()

    # Plot the grouped bars
    bar1 = ax.bar(index - bar_width/2, Marks, bar_width, label='student marks')
    bar2 = ax.bar(index + bar_width/2, avg_marks_of_all_student, bar_width, label='avg marks')

    # Add labels, title, and legend
    ax.set_xlabel('Exams',fontdict={'family': 'serif', 'size': 14,'color':'blue'})
    ax.set_ylabel('Scores',fontdict={'family': 'serif', 'size': 14,'color':'blue'})
    ax.set_title('Student Scores by Exam',fontdict={'family': 'serif', 'size': 17})
    ax.set_xticks(index)
    ax.set_xticklabels(Exams)
    ax.legend()
    plt.grid(True)
    plt.savefig("./.images/comparison.png")
    plt.clf()

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

elif purpose=="compare":
    s1=sys.argv[2]
    s2=sys.argv[3]

    data=pd.read_csv('main.csv')
    s1_data=data[data.Roll_Number == s1.lower()]
    s2_data=data[data.Roll_Number == s2.lower()]

    with open("main.csv") as f:
        header=f.readline().strip()
    header=header.split(",")[2:]
    
    s1_name=s1_data.Name.values[0]
    s1_marks=[]
    s1_rank=[]
    s2_name=s2_data.Name.values[0]
    s2_marks=[]
    s2_rank=[]
    

    for x in header:
        allstudentmarks=data[f"{x}"]
        allstudentmarks.replace('a', 0, inplace=True)
        allstudentmarks = pd.to_numeric(allstudentmarks)
        
        m=s1_data[f"{x}"].values[0]
        if(f"{m}"!="a"):
            s1_marks.append(float(m))       
        else:
            s1_marks.append(0)
        
        s1_rank.append(len(allstudentmarks[allstudentmarks>s1_marks[-1]])+1)


        m=s2_data[f"{x}"].values[0]
        if(f"{m}"!="a"):
            s2_marks.append(float(m))
        else:
            s2_marks.append(0)
        
        s2_rank.append(len(allstudentmarks[allstudentmarks>s2_marks[-1]])+1)

        
        

    # Define the width of the bars
    bar_width = 0.35

    # Define the x locations for the groups
    index = np.arange(len(header))

    # Create the figure and axes objects
    fig, ax = plt.subplots()

    # Plot the grouped bars
    bar1 = ax.bar(index - bar_width/2, s1_marks, bar_width, label=f'{s1_name}')
    bar2 = ax.bar(index + bar_width/2, s2_marks, bar_width, label=f'{s2_name}')

    # Add labels, title, and legend
    ax.set_xlabel('Exams',fontdict={'family': 'serif', 'size': 14,'color':'blue'})
    ax.set_ylabel('Scores',fontdict={'family': 'serif', 'size': 14,'color':'blue'})
    ax.set_title('Marks comparison',fontdict={'family': 'serif', 'size': 17})
    ax.set_xticks(index)
    ax.set_xticklabels(header)
    ax.legend()
    plt.grid(True)
    plt.savefig("./.images/comparison_s1_s2.png")
    plt.clf()

    ###########################################################################################