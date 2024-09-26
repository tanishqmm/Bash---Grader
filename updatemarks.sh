#!/bin/bash

#take name of student from user as input
echo -n "Name of student :"
read Name

#take roll number of student from user as input
echo -n "Roll_Number of student :"
read Roll_Number

#iterates through all csv files
for exam in  *.csv;do
    
    ##takes exam name from (exam).csv format
    examName=$(echo $exam | cut -d'.' -f1)

    ##check if he is present in exam. if present then grep output will be non-empty
    present_in_that_exam=$(grep -i "^$Roll_Number," "$exam") 
    
    ##true when person is present in that exam 
    if [[ $exam != "main.csv" ]] ; 
    then
        #if its present then
        if  [ -n "$present_in_that_exam" ]; then
            
            real_name=$(echo $present_in_that_exam | cut -d, -f2)
            if [ "${real_name,,}" == "${Name,,}" ]; then
        
                #Takes input if want to update marks or not 
                echo -n "want to update marks in $examName (Y or N / y or n) :"
                read want_to_change
                
                ##if want_to_change is y or Y
                if [[ ${want_to_change,,} == "y" ]]; ## {....,,}that convert it into lower case
                then
                    echo -n "Updated marks in $examName :"
                    ##ask user to give updated marks
                    read final_marks
                    ##only updates the mark if marks are of neumeric format 
                    if [[ "$final_marks" =~ ^[0-9]+$ ]]; then
                        ##This just updates marks in that exam.csv file
                        sed -i -E "s/^($Roll_Number,[A-Za-z ]*),.*/\1,$final_marks/I" $exam
                    else
                        echo "Updated marks in invalid format"
                    fi
                fi
            else
                echo "The given name doesn't match with the name of the student"
                exit 1
            fi





        else 
            ##If the person is absent then it tells that person was absent and if they want to add his entry or not 
            echo -n "He/she was absent in the $examName exam according to data.Do you want to add his/her record.(Y or N / y or n) :"
            read want_to_add

            if [[ ${want_to_add,,} == "y" ]]; then
                ##If want to add then give mark as input and then it append it in file
                echo "Marks given :"
                read marks
                echo "${Roll_Number,,},${Name},$marks">>$exam    
            fi
        fi    
    fi
done
##If main.csv exist then this part is to modify main.csv
if [ -e "main.csv" ];then	
    ##Internal field separator set to ","
    IFS=","
    #Reads first line of main.csv
    read -ra headers <<< "`head -1 main.csv`"

    #Slice it such that we only get name of exams which are currently in main.csv
    filestocombine=${headers[@]:2}
    length=${#filestocombine[@]}
   
    ##if last column is of "total" then we use modified combine ignoring last element
    if [ ${filestocombine[${length}-1]} == "total" ];then       
        bash submission.sh combine ${filestocombine[@]:0:$length-1}
    else
        #we use modified combine for all elements
        bash submission.sh combine ${filestocombine[@]}
    fi
fi

