import requests as rq
from pyquery import PyQuery as pq
import os
import logging
import when
from .tools import decode_ip_ref as dif
from . import Vpn,session

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',filename='myapp.log')
log = logging.getLogger(__name__)

URL = 'http://www.freeproxylists.net/zh/?c={}&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=0'

HEADERS={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Host':'www.freeproxylists.net',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
}

def req_content(baseurl,*index):
    """
    save url content to file
    :param baseurl:
    :param index:
    :return: content string
    """
    filename = '_'.join(['vpns', str(when.today()),'cont.txt'])
    if not os.path.isfile(filename):
        log.info("begin to request url")
        tx = rq.get(baseurl.format(*index),headers=HEADERS).text
        with open(filename,'w') as f:
            f.write(tx)
    else:
        log.info("today content file already exist, do not to request")

    with open(filename,'r') as f:
        return f.read()


def _str2tds(tds):
    if len(tds)<10 :
        log.error('tr width small than 10')
        return None
    ip = pq(dif(pq(tds[0])('a').text())).text()
    port = pq(tds[1]).text()
    protocol = pq(tds[2]).text()
    anony = pq(tds[3]).text()
    country = pq(tds[4]).text()
    region = pq(tds[5]).text()
    city = pq(tds[6]).text()
    available = pq(tds[7]).text().strip('%')
    respeed = pq(tds[8]).find('span.bar').css('width')
    trspeed = pq(tds[9]).find('span.bar').css('width')
    return Vpn(ip,port,protocol,anony,country,region,city,available,respeed,trspeed)


def parse_ct2entity(content):
    trs = pq(content).find('table.DataGrid tr')
    entities = []
    for tr in trs[1:]:
        tds = pq(tr).find('td')
        entities.append(_str2tds(tds))
    return entities

def parse_ct2option(content):
    options = pq(content)('select[name="c"]').find('option')
    country_index = [(pq(i).val(),pq(i).text()) for i in options if pq(i).val() is not '']
    return country_index

def run_pool():
    ctt = req_content(URL,'CN')
    #获得所有国家名字-简称
    ctry_kv = parse_ct2option(ctt)
    log.debug(ctry_kv)
    #获取不同国家的vpn信息
    entites = parse_ct2entity(ctt)
    log.debug(entites)