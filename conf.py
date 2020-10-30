import requests

API_KEY = 'EAA6ADAF-24E4-468D-8BDA-995B25723203'
MAX_WORKERS = 10
TIMEOUT = 6
MAX_RETRIES = 1

IP = requests.get('https://api.ipify.org/?format=json').json()['ip']

IP_RE = r'((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9]))'

BANNED_HEADERS = list(map(lambda x: 'HTTP_' + x, [
    'VIA',
    'FORWARDED',
    'FORWARDED-FOR',
    'X-FORWARDED',
    'X-FORWARDED-FOR',
    'X-HOST',
    'X-REAL-IP',
    'X-VIA'
]))
