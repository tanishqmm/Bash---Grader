#!/bin/bash

#path contains the path of gitrepodirectory
path=$(cat .gitrepoloc)
#this contain the current branch name
currentbranch=$(cat .currentbranch.txt)

#16 digit HASH value is generated using awk rand function
Hash_value=`awk -v seed=$RANDOM "BEGIN{srand(seed); print int(rand()*(9999999999999999-1000000000000000+1))+1000000000000000}"`

##taking the hash value of head position
currentcommit=$(cat $path/.head.txt)


##this array will store which files are modified or new  as compared to files present in head commit
declare -a Modified_files=()
declare -a New_files=()

##this array stores which files are deleted from head commit
declare -a deletedfiles=()

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


if [ -n "$currentcommit" ];then  
    
    ##it iterates over all the csv files in head commit and check if there exist a file in current directory with that particular name 
    #if the file name do not exist then it is deleted 
    for x in `ls $path/$currentbranch/$currentcommit/*.csv`
    do
        file=`basename $x`
        if [ ! -n "$(ls *.csv|grep "^$file$")" ];then
            deletedfiles+=("$file")
        fi        
    done
fi

##If all the array are empty then no changes are made in all csv files .. so it will not allow it to make commit
if [ ${#New_files[@]} -eq 0 ] && [ ${#Modified_files[@]} -eq 0 ] && [ ${#deletedfiles[@]} -eq 0 ];then
    echo "No changes have been"
else
    ##Displaying name of all files which have been modified or are new or are deleted compared to previous commit
    if [ ${#deletedfiles[@]} -gt 0 ];then
        echo Files deleted compared to previous commit :${deletedfiles[@]}
    fi
    if [ ${#New_files[@]} -gt 0 ];then
        echo New files :${New_files[@]}
    fi
    if [ ${#Modified_files[@]} -gt 0 ];then
        echo Modified :${Modified_files[@]}
    fi
fi