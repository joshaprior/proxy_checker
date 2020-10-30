import asyncio
import requests
import conf
import re


class Check:
    def __init__(self, pk, ip, port):
        self.pk = pk
        self.ip = ip
        self.port = port
        self.loop = asyncio.new_event_loop()

        self.tasks = []

        self.is_http = False
        self.is_https = False
        self.is_socks4 = False
        self.is_socks5 = False
        self.anonymity = ''

    def check(self):
        self.tasks.append(self.loop.create_task(self.http()))
        self.tasks.append(self.loop.create_task(self.https()))
        self.tasks.append(self.loop.create_task(self.socks4()))
        self.tasks.append(self.loop.create_task(self.socks5()))

        for task in self.tasks:
            self.loop.run_until_complete(task)
        print('updating...', self.ip, self.port)
        self.update()

    def update(self):
        params = {'api': conf.API_KEY}
        data = {
            'is_http': self.is_http,
            'is_https': self.is_https,
            'is_socks4': self.is_socks4,
            'is_socks5': self.is_socks5,
            'anonymity': self.anonymity
        }
        req = requests.post(f'http://127.0.0.1:8000/proxy/update/{self.pk}/', params=params, data=data)

    def check_anonymity(self, content):
        c = content.split('<pre>\r\n')[1].split('</pre>')[0].splitlines()
        h = dict(map(lambda x: x.split(' = '), c))
        addr = h['REMOTE_ADDR']

        anonymity = 'EL'

        if addr != self.ip:
            anonymity = 'DI'

        for (k, v) in h.items():
            if k.startswith('HTTP_'):
                if k in conf.BANNED_HEADERS:
                    anonymity = 'AN'
                if (m := re.findall(conf.IP_RE, v)):
                    m = m[0][0]
                    if m == conf.IP:
                        anonymity = 'TR'
                        break
                    elif m == self.ip:
                        anonymity = 'AN'
                        break
                    elif m != '127.0.0.1' or not m.startswith('10.'):
                        anonymity = 'DI'
                        break
        return anonymity

    async def http(self):
        for _ in range(conf.MAX_RETRIES):
            try:
                req = requests.get('http://azenv.net/', proxies={
                    'http': f'http://{self.ip}:{self.port}'
                }, timeout=conf.TIMEOUT)
                if req.status_code == 200:
                    self.is_http = True

                    self.anonymity = self.check_anonymity(req.text)

                    break
            except:
                pass

    async def https(self):
        for _ in range(conf.MAX_RETRIES):
            try:
                req = requests.get('https://azenv.net/', proxies={
                    'https': f'http://{self.ip}:{self.port}'
                }, timeout=conf.TIMEOUT)
                if req.status_code == 200:
                    self.is_https = True
                    break
            except:
                pass

    async def socks4(self):
        for _ in range(conf.MAX_RETRIES):
            try:
                req = requests.get('https://azenv.net/', proxies={
                    'https': f'socks4://{self.ip}:{self.port}'
                }, timeout=conf.TIMEOUT)
                if req.status_code == 200:
                    self.is_socks4 = True
                    break
            except:
                pass

    async def socks5(self):
        for _ in range(conf.MAX_RETRIES):
            try:
                req = requests.get('https://azenv.net/', proxies={
                    'https': f'socks5://{self.ip}:{self.port}'
                }, timeout=conf.TIMEOUT)
                if req.status_code == 200:
                    self.is_socks5 = True
                    break
            except:
                pass
