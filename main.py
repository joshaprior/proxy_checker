import requests
from concurrent.futures import ThreadPoolExecutor, wait
import conf
import checker

pool = ThreadPoolExecutor(max_workers=conf.MAX_WORKERS)

while 1:
    futures = []

    params = {'api': conf.API_KEY}

    req = requests.get('http://127.0.0.1:8000/proxy/10/', params=params)
    data = req.json()
    for proxy in data['proxies']:
        ip_address, port = proxy['fields'].values()
        futures.append(pool.submit(checker.Check(proxy['pk'], ip_address, port).check))

    wait(futures)
