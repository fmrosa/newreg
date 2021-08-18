import base64
from datetime import date, timedelta
import wget
import shutil
import os

'''https://whoisds.com//whois-database/newly-registered-domains/MjAyMS0wNy0xOS56aXA=/nrd'''

DS_URL = 'https://whoisds.com//whois-database/newly-registered-domains/$date/nrd'

# fetching yesterday's date in formar YYYY-MM-DD
yesterday = date.today()-timedelta(days=1)
yesterday = yesterday.strftime("%Y-%m-%d")+".zip"

# encoding to b64
yesterday = base64.b64encode(yesterday.encode()).decode()

# replace URL with the encoded date
DS_URL_TODAY = DS_URL.replace("$date", yesterday)

#print(DS_URL_TODAY) // just for tsting

date = date.today()-timedelta(days=1) 


#Create Data Dir if it doesn't exist
if not os.path.exists('my_folder'):
    os.makedirs('my_folder')
    
# download the file to /data folder
print("# downloading file")
wget.download(DS_URL_TODAY, f"./data/{date}.zip")

# unpack file in /data folder
print("")
print("# unpacking file")
shutil.unpack_archive(f"./data/{date}.zip", "./data")

# adjust names and remove archive
os.system(f"rm -f ./data/{date}.zip")
os.system(f"mv ./data/domain-names.txt ./data/{date}.txt")






