import asyncio
import aiohttp
import json
import sys
from itertools import islice
from datetime import date, datetime, timedelta

#Define Number of records to proccess at once
BATCH_SIZE = 15000

async def sitehead(index, session, url, outfile):
    try:
        async with session.head(("https://" + url)) as resp:
            print(index, url, str(resp.status))
            if resp.status == 200:
                print(url)
                with open(outfile, 'a') as f:
                    f.write(url + '\n')
    except:
        print(str(index), url)
        return

async def main():
    headtasks = []
    #Setup async call
    connector = aiohttp.TCPConnector(ssl=False, limit=1000)
    timeout = aiohttp.ClientTimeout(total=60000, sock_read=None, connect=5, sock_connect=1)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        #Define File to Open
        today = date.today()
        filedate = today-timedelta(days=1) 
        infile = sys.argv[1] if len(sys.argv) >= 2 else f'./data/{filedate}.txt'
        outfile = sys.argv[1] if len(sys.argv) >= 3 else f'./data/{filedate}_out.txt'
        print(outfile)
        with open(infile, 'r') as f1:
            while True:
                batch = [line.strip() for line in islice(f1, BATCH_SIZE)]

                if not batch:
                        # no more lines - we're done
                        break
                else: 
                    for index,line in enumerate(batch):
                        #line = line.strip()
                        #print(line)
                        head = asyncio.create_task(sitehead(index, session, line, outfile))
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