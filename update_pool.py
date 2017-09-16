import requests as rq
from pyquery import PyQuery as pq
import os
import logging
import when
from .tools import decode_ip_ref as dif

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

url = 'http://www.freeproxylists.net/zh'
HEADERS={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Host':'www.freeproxylists.net',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
}
logging.basicConfig()


if not os.path.isfile('tempfile.txt'):
    log.debug("begin to request")
    tx = rq.get('http://www.freeproxylists.net/zh/?c=CN&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=0',headers=HEADERS).text
    with open("tempfile.txt",'w') as f:
        f.write(tx)

with open("tempfile.txt",'r') as f:
    p = pq(f.read())

options = p('select[name="c"]').find('option')
country_index = [pq(i).val() for i in options if pq(i).val() is not '']

# class Vpn(object):


# 根据不同的index构造请求vpn地址
base_vpn_url = 'http://www.freeproxylists.net/zh/?c={}&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=0'
filename = '_'.join(['vpns',str(when.today())])
if not os.path.isfile(filename):
    with open(filename,'w') as f:
        f.write(rq.get(base_vpn_url.format('CN'),headers=HEADERS).text)

with open(filename,'r') as f:
    trs = pq(f.read().find('table.DataGrid tr'))
    for tr in trs[1:]:
        tds = pq(tr).find('td')
        print(tds)
