#!/bin/bash

#path contains the path of gitrepodirectory
path=$(cat .gitrepoloc)

#this contain the current branch name
currentbranch=$(cat .currentbranch.txt)

##if second argument is branch it means its for checkout from one branch to another branch
if [ $2 == "branch" ];then
    ##Error handling that branch name not provided
    if [ $# -le 2 ];then
        echo "Specify branch name"
        exit 1
    fi    
    #storing branch_name
    branchtocheckout=$3
    ##checks if the branch exists or not
    if [ ! -n "$(ls $path | grep "^$branchtocheckout$")" ]
    then
        echo "No such branch exist"
        exit 1
    fi

    ##take out last commit done in branch to which we have to do checkout
    last_commit_in_branch_to_checkout=$(cat $path/$branchtocheckout/.git_log | grep "commit: "|tail -1|cut -d" " -f2)

    #removes all csv files 
    rm *.csv
    #copy all files of that branch last commit to in current folder
    cp $path/$branchtocheckout/$last_commit_in_branch_to_checkout/*.csv . 

    ##updates corresponding txt file with their new values
    echo $branchtocheckout > .currentbranch.txt
    echo $last_commit_in_branch_to_checkout>$path/.head.txt
    
## if second argument is -m then checkout is to be done in same branch but with help of commit message
elif [ $2 == "-m" ];then
    #greps the content of git_log file with message starting from that text which is given to us then stores number of lines it have
    numlines=`grep "message: \"$3" $path/$currentbranch/.git_log|wc -l`

    ##if number of line is greater than 1 it imply two or more commits have same commit message starting from that particular text
    if [ $numlines -gt 1 ];then
        echo "conflict in message; more than one message start from this text"
    elif [ $numlines -eq 1 ];then
        ##if numlines is 1 then get the hash value of that using cut command 
        expected_checkout=`grep "message: \"$3" $path/$currentbranch/.git_log`
        Hash_value=`echo $expected_checkout | cut -d" " -f2`

        #removes all csv files
        rm *.csv
        #cp all files from that commit to current folder
        cp $path/$currentbranch/$Hash_value/*.csv .

        #updates head position
        echo $Hash_value>$path/.head.txt 
    else
        #if numline is 0 then no such commit mssg present
         echo "No such message present"   
    fi

##else means cmmit based on Hash value
else

    if [[ ! "$2" =~ ^[0-9]{3,}$ ]]; then
        echo "Hash value is neumerical and must contain at least 3 digits"
        exit 1
    fi
    
    Hash_value=$2
    #greps the content of git_log file with Hash starting from that text which is given to us then stores number of lines it have
    numlines=`grep "commit: $Hash_value" $path/$currentbranch/.git_log|wc -l`

    ##if numlines is more than 1 then conflict
    if [ $numlines -gt 1 ];then
        echo "conflict in hash values; more than one hash value start from this numbers" 
    elif [ $numlines -eq 1 ];then 
        ##if numlines is one
        expected_checkout=`grep "commit: $Hash_value" $path/$currentbranch/.git_log`
        Hash_value=`echo $expected_checkout | cut -d" " -f2`
        #removes all csv files
        rm *.csv
        #cp all files from that commit to current folder
        cp $path/$currentbranch/$Hash_value/*.csv .

        #updates head position
        echo $Hash_value>$path/.head.txt 
    else 
        #if numline is 0 then no such Hash value present
        echo "No such hash value present"    
    fi
fi