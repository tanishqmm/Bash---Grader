#!/bin/bash

#Checks if "combine" is the only argument passed 
if [ $1 == "combine" ] && [ $# -eq 1 ];then
    #if main.csv exist then run this
    if [ -e main.csv ]
    then
        #checks if first line of main.csv already contain "total" header  
        if [ -n "$(head -1 main.csv|grep "total")" ]
        then
            #if total is present then new main.csv will also contain "total"
            bash ./combine.sh
            #to add "total" column at end 
            bash submission.sh total
        else
            bash ./combine.sh
        fi    
    else
        #if main.csv not present then just combine all csv files
        bash ./combine.sh
    fi
##############################################################
##############################################################

elif [ $1 == "combine" ] && [ $# -gt 1 ];then  ##this is modified version of combine command
##In this along with command "combine" we will also pass those exams whose data must only be combined     
    args=("$@") #array of argument
    files=(${args[@]:1}) #slicing array such that we get name of files only (this slicing take array elements from 1st index to last, 0th index "combine" is not taken)

    ## same pattern follow except the fact that this files name are again pass to combine script as argument
    if [ -e main.csv ]
    then
        if [ -n "$(head -1 main.csv|grep "total")" ]
        then
            bash ./combine.sh ${files[@]}
            bash submission.sh total
        else
            bash ./combine.sh ${files[@]}
        fi    
    else
        bash ./combine.sh ${files[@]}
    fi

##############################################################
##############################################################

elif [[ $1 == "upload" ]];then #checks if first argument is upload
    if [ $# -eq 1 ] #Error handling 
    then
        echo "Please specify which file to upload."
    else
        #Copy the file specified by the path in secong argument into current directory  
        cp -r $2 ./
    fi

##############################################################
##############################################################

elif [[ $1 == "total" ]];then #checks if first argument is "total"
    #executes awk cript so that an total column is added which contains total of marks in each exam
    awk -f total.awk main.csv > .main
    #output of awk command is stored temporarily in .main file and then redirected to main.csv. temporary file is deleted at last
    cat .main > main.csv
    rm .main
        
##############################################################
##############################################################

elif [[ $1 == "update" ]];then #checks if first argument is "update"
    bash ./updatemarks.sh     #update.sh is executed  

##############################################################
##############################################################
##>>>>This part initiate git in directory
elif [[ $1 == "git_init" ]];then #checks if first argument is "git_init"
    
    if [ -e .gitrepoloc ];then ##if file name .gitrepoloc exist then git is already activated.... this file store address of remote repo
    echo "git already activated"  
    exit 1
    fi   

    if [ $# -eq 1 ]; then #Error handling -- where to make remote repo is not specified 
        echo "Please specify location of remote repository."
        exit 1
    fi
    if [ -e "$2" ];then
        rm -r $2
    fi
    ##Executes git_init.sh with path of remotr repository  pass as argument
    bash git_init.sh "$2"
##############################################################
##############################################################
##>>>>This part creates commit
elif [[ $1 == "git_commit" ]];then
    
    if [ ! -e ".gitrepoloc" ];then
        echo "git_init has not been executed yet." ##checks if git init has been perfored already or not
        exit 1
    fi

    if [ ! $# -eq 3 ] || [ ! $2 == "-m" ];then ##Error handling of syntax
        echo "ERROR!!!!>>> Usage : git submission.sh git_commit -m '<message>' "
        exit 1
    fi

    bash git_commit.sh "$3" 
    
##############################################################
##############################################################
##>>>>This part is for performing checkout
elif [ $1 == "git_checkout" ];then


    if [ $# -eq 1 ] ##Error handling
    then
        echo "specify Hash value or commit message or branchname"
        exit 1
    fi

    #path contains the path of gitrepodirectory
    path=$(cat .gitrepoloc)
   
    #this contain the current branch name
    currentbranch=$(cat .currentbranch.txt)


    ##taking the hash value of head position
    currentcommit=$(cat $path/.head.txt)

    ##this array will store which files are modified or new  as compared to files present in head commit
    declare -a Modified_files=()
    declare -a New_files=()

    ##this array stores which files are deleted from head commit
    declare -a deletedfiles=()

    ##currentcommit will be empty only when we havent made any commit yet
    ##If currentcommit means head position is present(not empty) then only we will allow to checkout
    if [ -n "$currentcommit" ];then 
        ##iterates over all the csv files present in current directory
        for x in *.csv
        do 
            #if the file exist in head commit and its diff is nonempty then the file is modified 
            if [ -e $path/$currentbranch/$currentcommit/$x ];
            then
                if [ -n "`diff -q $x $path/$currentbranch/$currentcommit/$x`" ];
                then
                    Modified_files+=("$x")  
                fi
            ##if this file doesn't exist in head commit then it must be New file
            else 
                    New_files+=("$x")
            fi
        done 
        
        ##it iterates over all the csv files in head commit and check if there exist a file in current directory with that particular name 
        #if the file name do not exist then it is deleted 
        for x in `ls $path/$currentbranch/$currentcommit/*.csv`
        do
            file=`basename $x`
            if [ ! -n "$(ls *.csv|grep "^$file$")" ];then
                deletedfiles+=("$file")
            fi        
        done
    
        ##if there are no changes in csv files then only allow to checkout otherwise changes will be lost
        if [ ${#New_files[@]} -eq 0 ] && [ ${#Modified_files[@]} -eq 0 ] && [ ${#deletedfiles[@]} -eq 0 ];then
            bash git_checkout.sh "$@"
        else
            echo "Commit before you do checkout otherwise your work will be gone"    
        fi
    else
        echo "you havent made any commit to do any kind of checkout"
    fi
      
##############################################################
##############################################################
##>>>>This part creates newbranch
elif [ $1 == "git_newbranch" ];then
    if [ $# -eq 1 ];then
        echo "please provide branch name"
        exit 1
    fi

    #path contains the path of gitrepodirectory
    path=$(cat .gitrepoloc)
   
    #this contain the current branch name
    currentbranch=$(cat .currentbranch.txt)

    
    ##taking the hash value of head position
    currentcommit=$(cat $path/.head.txt)

    newbranch_name=$2
    ##currentcommit will be empty only when we havent made any commit yet
    ##if currentcommit is not empty then only newbranch will be created otherwise it will just rename existing branch
    if [ -n "$currentcommit" ]
    then
        ##checks if branch name already exist or not
        if [ -n "$(ls $path | grep "^$newbranch_name$")" ]
        then            
            echo "This branch name have been already taken plz use another name"
            exit 1
        fi
        ##Create new branch just by copying current branch directory into directory of name with newbranch
        cp -r $path/$currentbranch $path/$newbranch_name

    else
        ##If currentcommit means head position is not present then creating new branch will just change branch name of current branch
        mv $path/$currentbranch $path/$newbranch_name 
        #update in current branch name
        echo $newbranch_name > .currentbranch.txt
    fi

##############################################################
##############################################################
##>>>shows all the commit data in terminal
elif [ $1 == "git_log" ]; then
    path=$(cat .gitrepoloc)
    currentbranch=$(cat .currentbranch.txt)
    #just print what we have written in gi_log file
    cat "$path/$currentbranch/.git_log"

##############################################################
##############################################################

elif [ $1 == "git_branch" ]; then
        #path contains the path of gitrepodirectory
    path=$(cat .gitrepoloc)
   
    #this contain the current branch name
    currentbranch=$(cat .currentbranch.txt)
    
    ##Shows all the branch present  
    ls $path |cat |sed -E "s/^($currentbranch)$/*\1/g"


##############################################################
##############################################################

elif [ $1 == "git_status" ]; then
    ## show status of changes in all file compared to head position
    bash git_status.sh
##############################################################
##############################################################

elif [ "$1" == "stats" ]; then
    args=("$@")
    ##in this first argument will be the purpose of using stats 
    ##purpose can be "student" to get stats of that particular student or "compare" to compare two roll numbers
    
    python3 plotgenerator.py ${args[@]:1} ##generate graphs 
    python3 statspresentation.py ${args[@]:1} #display information  in nice format

##############################################################
##############################################################

elif [ $1 == "grades" ];then
    ## this will show frequency chart of grade system and also creates grades.txt for whichever exam you click
    #the thing written in command substitution is use to give all exam names in current directory whose .csv is present except for main.csv
    python3 grader.py $(ls *.csv|sed 's/main.csv//g'|sed -E 's/([a-zA-Z0-9]+).csv/\1/g')

##############################################################
##############################################################

elif [ $1 == "examstats" ]; then
    ##it will show detail analysis of exams
    #the thing written in command substitution is use to give all exam names in current directory whose .csv is present except for main.csv
    python3 examstats.py $(ls *.csv|sed 's/main.csv//g'|sed -E 's/([a-zA-Z0-9]+).csv/\1/g')
##############################################################
##############################################################

elif [ $1 == "calculate_cpi" ]; then
    ##just run it to know what it do :-)
    python3 cpicalculator.py
fi
