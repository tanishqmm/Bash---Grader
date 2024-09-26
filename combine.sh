#!/bin/bash

##declare array and distros
declare -a name_of_exams
declare -a Roll_numbers
declare -A Name
declare -a results

##results is the array which conatin exam name whose data we have to combine
if [ $# -ge 1 ]; then
    results=("$@") #if arguments are present then exam names are list of arguments
else 
    results=*.csv    #else all exams will be cosidered for combining data
fi

##iterating through all exams
for result in  ${results[@]};do		
		Exam_name=`echo $result | cut -d"." -f1` #storing name of exam that is if result is midsem.csv then Exam_name is midsem
        if [[ ! $Exam_name == "main" ]] && [ -e "$Exam_name.csv" ];then
    		name_of_exams+=("$Exam_name") ##storing all the exam names in an array
        
            i=1

            while read -r line || [ -n "$line" ];do
                
                if [ $i -eq 1 ];then
                    ##this is to skeep first line which of header in all files
                    i=$[i+1]
                else    
                    #cut our Roll number from eqach line
                    Roll_number=$(echo $line|cut -d, -f1)
                    #this checks whether the given roll number is already present in the array  Roll_numbers  and then takes its negation
                    #if roll number is not present in array then it adds it in our array 
                    if [[ ! " ${Roll_numbers[@]} " =~ " ${Roll_number,,} " ]];then
                        Roll_numbers+=("${Roll_number,,}") #we add roll numbers in array in lowercase                       
                        Name[${Roll_number,,}]=$(echo $line|cut -d, -f2) #we also store name of that personn as value with key as its roll number
                    fi	
                fi
            done < "$Exam_name.csv"
        fi
done

##############################################################
##############################################################

#creating of header by adding comma separated name of exams in list 
heading="Roll_Number,Name"
for exam in ${name_of_exams[@]};do 
    heading+=",$exam"
done
#redirecting of headeer in main.csv
echo $heading > main.csv

##############################################################
##############################################################

#Iterating through Roll_Numbers which we have store
for roll in ${Roll_numbers[@]};do
    #"performace" variable will be final variable which we will append in main.csv file
    performance="$roll,${Name[${roll}]}" #initialize it with "rollnumber,name" of that person
    ##iterating through all the exam files whose data we have to combine
    for file in ${name_of_exams[@]};do
        content=$(grep -i "^$roll," $file.csv) #if that roll number is present in that file.csv then "content" will have value equal to its whole row (roll,name,marks) 
                                               #if that roll number is not present then "content" will be empty string
        if [[ -z $content ]];then
            #if content is empty it means he/she was absent so append ",a"
            performance+=",a"
        else
            
            #else append ",marks" 
            marks=$(echo $content | cut -d, -f3)
            performance+=",${marks%$'\r'}"
        fi

    done
    echo $performance >> main.csv ##appends performance of that roll number in main.csv
done

