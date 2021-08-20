#!/usr/bin/env python3
import asyncio
import aiohttp
import json
import sys
from itertools import islice
from datetime import date, datetime, timedelta

#Define Number of records to proccess at once
BATCH_SIZE = 1000

async def sitehead(session, url):

    try:
        async with session.head(("https://" + url)) as resp:
            #print(url, str(resp.status))
            if resp.status == 200:
                return(url)
                #with open(outfile, 'a') as f:
                #    f.write(url + '\n')
    except:
        return


async def setoolspost(index, session, rbiurls):
    rbiurls = json.dumps(rbiurls)
    if index == 1:
        params = {'init': 'true'}
    else:
        params = {'append': 'true'}
    #print(rbiurls)
    setools = "https://setools.netskope.io/api/v1/file/rbiurls/"
    headers = {'Authorization': 'Token ydwXBxilYFD1yap97XxAUuggt8GGR3g3uq8WBqxHsnmV1Ad4uG'}
    resp = await session.post(setools, data=rbiurls, headers=headers, params=params)
    #print(await resp.json())
    with open("./logs/log_" + filedate, 'a') as f:
                    f.write(await resp.json())


async def getbatch(index, batch):
    headtasks = []
    #Setup async call
    connector = aiohttp.TCPConnector(ssl=False, limit=None)
    timeout = aiohttp.ClientTimeout(total=None, sock_read=None, connect=None, sock_connect=.5)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        for line in batch:
            head = asyncio.create_task(sitehead(session, line))
            headtasks.append(head)
        #Run Tasks
        headresults = await asyncio.gather(*headtasks)
        results = filter(None, headresults)
        results = list(results)
        #print(results)
        await setoolspost(index, session, results)

async def main(): 
    #Define File to Open
    today = date.today()
    filedate = today-timedelta(days=1) 
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'./data/{filedate}.txt'
    outfile = sys.argv[1] if len(sys.argv) >= 3 else f'./data/{filedate}_out.txt'

    with open(infile, 'r') as f1:
        index = 0
        while True:
            index +=1
            batch = [line.strip() for line in islice(f1, BATCH_SIZE)]

            if not batch:
                    # no more lines - we're done
                    break
            else: 
                await getbatch(index, batch)
                #print(batch)
                #for index,line in enumerate(batch):



  
asyncio.run(main())
