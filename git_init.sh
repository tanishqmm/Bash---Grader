#!bin/bash

mkdir "$1"  

mkdir "$1"/master ##master branch created in git repodir
touch "$1"/master/.git_log ## makes .git_log file in remote repository
touch $1/.head.txt #this will store our current position

echo "master" > .currentbranch.txt ## hidden file currentbranch.txt will store the current branch name 
echo "$1" > .gitrepoloc ##This file is created at time when git_init runs for first time. It stores address of remote repository. 

echo -e "Initialized empty Git repository in "$1" \ncurrently on master branch"
