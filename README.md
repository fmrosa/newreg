# newreg

NewReg fetches the latest registered domains from whoisds.com and puts it on a txt file. 
After that, it creates a CSV file adding to each entry the information below: 

- date added
- domain length
- tld
- if it has a number 
- if it has dashes

Only non-std library used was wget so before using:

> pip3 install wget 

and then to use it: 

> python3 download_domains.py

then

> python3 add_domains_db.py

this will create a file on a /data folder that is named like **%YYYY%mm%dd.csv**. 
All other files that were used to create the csv are deleted after processing
