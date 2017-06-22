How to run:

python apriori.py -f bank.csv -s 0.33 -c 1.00 -d ';' -p 1

-f is for the file name 
-s is for the support interval
-c is for the confidence interval
-d is for the delimiter used in the database dump
-p is for the parsing options within the data dump. 1 is when the columns are not relevant (non-unique). 2 is for when the columns are relevant, and 3 is for when the columns are relevant and the first line in the dump is the name of the columns
