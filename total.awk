BEGIN {
    ##Set the field seperator and output field separator
    FS=","
    OFS=","
    is_total_column_present=0
}
NR==1 {
    ##if total is present then it will set value of is_total_column_present=1
    if ($0~/total/){
        print $0;
        is_total_column_present=1;
    }
    else{
        print $0,"total";
    }
}
NR>1 {
    ##Depending on the value of is_total_column_present it will work differently
    if (is_total_column_present==0){

        ##if total is not present then will calculate sum till last column
        sum=0
        for(i=3;i<=NF;i++){
            if ($i!="a"){
               
                sum+=($i);
            }
        }
        print $0,sum;  
    }
    else {
        ##if total is present then will calculate sum till last second column (ignoring total column)
        sum=0;
        printf $1","$2",";
        for(i=3;i<NF;i++){
            if ($i!="a"){
                sum+=($i);
            }
            printf $i",";
        }
        printf sum"\n";
    }  
}
