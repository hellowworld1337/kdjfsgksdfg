import aiohttp
import asyncio
import json
from time import sleep
import random
import string
from bs4 import BeautifulSoup
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
from multiprocessing.dummy import Pool
import numpy as np
from loguru import logger
from random import shuffle

async def main(proxys: list):
    with open("names.txt", "r") as f:
        newnames=[i.replace("\n", "") for i in f.readlines()]
    #proxy_auth = aiohttp.BasicAuth(username, password)
    for proxy in proxys:
        logger.info(f"start proxy: {proxy}")
        for i in range(3):
            try:
                emailfun = lambda: ''.join([random.choice(string.ascii_letters) for i in range(random.randint(10, 23))]) + "@gmail.com"
                nick = lambda: ''.join([random.choice(string.ascii_letters) for i in range(random.randint(10, 23))])
                sitekey = '6Ley_EofAAAAAJVfLglMetw5fBPfXvItYYueYTta'
                connector = ProxyConnector.from_url(proxy)
                #print(connector)
                async with aiohttp.ClientSession(connector=connector) as session:
                    
                    async with session.post(f"https://api.capmonster.cloud/createTask", json={
                    "clientKey":"a565c9c0a00fbc914c6463214f56b9f3",
                    "task": {
                        "type":"RecaptchaV2EnterpriseTaskProxyless",
                        "websiteURL":"https://marginfi.canny.io/",
                        "websiteKey": sitekey,
                    }
                    }) as captcha:
                        idcapth = json.loads(await captcha.text())
                        #print(idcapth)
                        while True:
                            sleep(5)
                            async with session.post(f"https://api.capmonster.cloud/getTaskResult",json={
                                "clientKey":"a565c9c0a00fbc914c6463214f56b9f3",
                                "taskId": idcapth['taskId']
                            }) as captchtoken:
                                token = json.loads(await captchtoken.text())
                                #print(token)
                                if token['status'] == 'ready':
                                    gRecaptchaResponse = token['solution']['gRecaptchaResponse']
                                    print("Каптча решена")
                                    break
                        json_data = {
                'captcha': {
                    'value': gRecaptchaResponse,
                    'version': 'v2',
                },
                'email': emailfun(),
                'name': random.choice(newnames),
                'password': 'kruglovpapa1',
            }
                        #print(json_data)
                        async with session.post('https://marginfi.canny.io/api/viewer/signup', json=json_data) as response:
                            if response.status == 200:
                            #print(f"{response.status} | {await response.text()}")
                                logger.success(f"Успешная рега аккаунта {response.status} | {await response.text()}")
                            else:
                                logger.error(f"Ошибка реги аккаунта {response.status} | {await response.text()}")
                                pass
                        async with session.get('https://marginfi.canny.io/memecoin-listings') as resppage:
                            
                            soup = BeautifulSoup(await resppage.text(), 'html.parser')
                            scripts = soup.find_all('script')
                            for script in scripts:
                                if 'csrfToken' in script.text:
                                    csrfroken = str(script.text.strip().split("csrfToken")[1].replace(' }, "voteQueries": {}, "voters": {} };', '').replace('": "','').replace('"','').strip().replace('},voteQueries:{},voters:{}};','').replace(':',''))
                            #print(csrfroken)
                        json_data = {
                'csrfToken': csrfroken,
                #'__canny__browserTheme': 'dark',
                #'__canny__experimentID': 'a4b7cca5-1528-971e-e574-709310132189',
                #'__canny__requestID': 'fa8c171e-134f-57db-d8f1-e3eb6c79f2f9',
                '__host': 'marginfi.canny.io',
                #'__canny__sessionID': 'bfa3da40-a465-d7e2-bef7-4b252a63d615',
                #'__canny__userID': '659ad9ae36d4cc31cfc082e6',
                'boardID': '6597106e641693db08a38a8d',
                'postURLName': 'drago',
            }
                        async with session.post('https://marginfi.canny.io/api/posts/getOne', json=json_data) as respcheck:
                            check = await respcheck.json()
                            print(f"Количество голосов до: {check['post']['score']}")
                        for i in range(1):
                            json_data = {
                    'csrfToken': csrfroken,
                    'postID': '65972389199d09572fa5942e',
                    'score': 1,
                }
                            async with session.post('https://marginfi.canny.io/api/posts/vote',json=json_data) as response:
                                print(f"{response.status} | {await response.text()}")
                        
                        json_data = {
                'csrfToken': csrfroken,
                #'__canny__browserTheme': 'dark',
                #'__canny__experimentID': 'a4b7cca5-1528-971e-e574-709310132189',
                #'__canny__requestID': 'fa8c171e-134f-57db-d8f1-e3eb6c79f2f9',
                '__host': 'marginfi.canny.io',
                #'__canny__sessionID': 'bfa3da40-a465-d7e2-bef7-4b252a63d615',
                #'__canny__userID': '659ad9ae36d4cc31cfc082e6',
                'boardID': '6597106e641693db08a38a8d',
                'postURLName': 'drago',
            }
                        async with session.post('https://marginfi.canny.io/api/posts/getOne', json=json_data) as respcheck:
                            check = await respcheck.json()
                            print(f"Количество голосов после: {check['post']['score']}")
            except Exception as e:
                print(f"Какакя то ошибка: {e}")
                pass



def mainmain(kek:dict):
    new = [i.replace("\n", "") for i in kek['proxy']]
    asyncio.run(main(new))


if __name__ == '__main__':
    with open("proxys.txt", "r") as file:
        lines = file.readlines()
    newest = []
    for i in lines:
        new = i.split(':')
        newest.append(f"http://{new[2]}:{new[3]}@{new[0]}:{new[1]}".replace("\n", ""))
    #print(newest)
    # with open("proxys.txt", "r") as file:
    #     lines = file.readlines()
    shuffle(newest)
    splits = np.array_split(newest, 10)

    newlist = []

    for proxy in splits:
        newlist.append({'proxy':list(proxy),})

    with Pool(processes=10) as executor:
        executor.map(mainmain, newlist)
