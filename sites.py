import asyncio
import aiohttp
import json
from itertools import islice
from datetime import date, datetime, timedelta

#Define Number of records to proccess at once
BATCH_SIZE = 15000

async def sitehead(index, session, url):
    try:
        async with session.head(("https://" + url)) as resp:
            print(url, str(resp.status))
    except:
        #print(str(index))
        return

async def main():
    headtasks = []
    #Setup async call
    connector = aiohttp.TCPConnector(ssl=False, limit=1000)
    timeout = aiohttp.ClientTimeout(total=60000, sock_read=None, connect=5, sock_connect=1)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        #Define File to Open
        filedate = date.today()-timedelta(days=1) 
        file = f'./data/{filedate}.txt'
        with open(file, 'r') as f1:
            while True:
                batch = [line.strip() for line in islice(f1, BATCH_SIZE)]

                if not batch:
                        # no more lines - we're done
                        break
                else: 
                    for index,line in enumerate(batch):
                        #line = line.strip()
                        #print(line)
                        head = asyncio.create_task(sitehead(index, session, line))
                        headtasks.append(head)

                    #Run Tasks
                    starttime = datetime.utcnow()
                    print("**Starting Batch: " + str(starttime))
                    headresults = await asyncio.gather(*headtasks)
                    endtime = datetime.utcnow() - starttime
                    print("Ending Batch:" + str(endtime))

starttime = datetime.utcnow()      
asyncio.run(main())
endtime = datetime.utcnow() - starttime
print("Ending Batch:" + str(endtime))