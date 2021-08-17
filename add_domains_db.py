# add the csv file to sqlite
# # https://mungingdata.com/sqlite/create-database-load-csv-python/

from datetime import date, timedelta
import os
import re
import csv
import requests

# determine yesterday's date
yesterday = date.today()-timedelta(days=1)
yesterday = yesterday.strftime("%Y-%m-%d")

# define the data transformations 

def length(domain):
    dot = domain.find(".")
    site = domain[:dot-1]
    return len(site)

def tld(domain):
    domlen = len(domain)
    dot = domain.find(".")
    tld = domain[dot+1:domlen]
    return tld

def hasnum(domain):
    if re.search(r'\d', domain):
        return 1
    else: 
        return 0

def hasdash(domain):
    if re.search(r'-', domain):
        return 1
    else: 
        return 0

def dnsresolves(domain):
    params = {"name": domain, "type": "A"}
    resolution = requests.get("https://dns.google.com/resolve", params=params)
    status = resolution.json()['Status']
    print(status)



# opening file1 in reading mode and file2 in writing mode
date = date.today()-timedelta(days=1) 
file = f'./data/{date}.'

with open(file+'txt', 'r') as f1, open(file+'csv', 'w') as f2:
    reader = f1.read().splitlines()
    writer = csv.writer(f2, delimiter=',')
    # add header
    header = ['domain','dateAdd','length','tld','hasNum','hasDash','isAlive']
    writer.writerow(i for i in header)

    # loop through the lines in file1 and write functions in file2 
    for line in reader: 
        writer.writerow([line, date, length(line), tld(line), hasnum(line), hasdash(line)])
        dnsresolves(line)

    # no need to close the file - already closed. 

#remove original file 
os.system(f'rm -f ./data/{date}.txt')





