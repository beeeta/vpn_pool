import requests as rq
from pyquery import PyQuery as pq
import os
import logging
import when
from .tools import decode_ip_ref as dif
from . import Vpn,session
import re

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',filename='myapp.log')
log = logging.getLogger(__name__)

URL = 'http://www.freeproxylists.net/zh/?c={}&page={}'

HEADERS={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Host':'www.freeproxylists.net',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
}

def vali_ctt(ctt):
    if pq(ctt).find('input[name="recaptcha_response_field"]').size()>0:
        log.debug('get a invalidate content')
        return 1
    else:
        return 0

def req_content(baseurl,refresh=False,*index):
    """
    save url content to file
    :param baseurl:
    :param index:
    :return: content string
    """
    filename = '_'.join(['vpns', index[0], str(when.today()), 'raw.txt'])
    if refresh or not os.path.isfile(filename):
        log.info("begin to request url")
        tx = rq.get(baseurl.format(*index),headers=HEADERS).text
        # 检验tx是否为有效的内容，如果ip已被屏蔽，需要使用匿名代理进行请求
        if vali_ctt(tx)>1:
            pass # TODO
        with open(filename,'w') as f:
            f.write(tx)
    else:
        log.info("today content file already exist, do not to request")

    with open(filename,'r') as f:
        ctt = f.read()
        div_page = pq(ctt)('div.page')
        if div_page.size() >0:
            print('div_page is not none')
            print(len(div_page.find('a')))
            return ctt,len(div_page.find('a'))-2 # 上一页，下一页
        print('div_page is not exist')
        return f.read(),1


def _str2tds(tds):
    if len(tds)<10 :
        log.error('tr width small than 10')
        return None
    row_txt = pq(tds[0]).text()
    # cpl = re.compile()
    res = re.search(r'"(.*)"',row_txt,)
    ip = pq(dif(res.group().strip("\""))).text()
    port = pq(tds[1]).text()
    protocol = pq(tds[2]).text()
    anony = pq(tds[3]).text()
    country = pq(tds[4]).text()
    region = pq(tds[5]).text()
    city = pq(tds[6]).text()
    available = pq(tds[7]).text().strip('%')
    respeed_style = pq(tds[8]).find('span.bar').attr('style')
    respeed = float(re.search(r"(?<=(width:))(\d{0,3})(?=(%))",respeed_style).group())
    trspeed_style = pq(tds[9]).find('span.bar').attr('style')
    trspeed = float(re.search(r"(?<=(width:))(\d{0,3})(?=(%))",trspeed_style).group())
    return Vpn(ip,port,protocol,anony,country,region,city,available,respeed,trspeed)

def parse_ct2entity(content):
    trs = pq(content).find('table.DataGrid tr')
    entities = []
    for index,tr in enumerate(trs[1:]):
        tds = pq(tr).find('td')
        entity = _str2tds(tds)
        if entity is not None:
            entities.append(entity)
        else:
            log.debug('the tr index:{} is unformat'.format(index))
    return entities

def parse_ct2option(content):
    options = pq(content)('select[name="c"]').find('option')
    country_index = [pq(i).val() for i in options if pq(i).val() is not '']
    return country_index

def save_by_ctry_key(key):
    ctt,total = req_content(URL,key,1)
    save_one_page(ctt)
    cur = 1
    while total > cur:
        ctt, total = req_content(URL, key, cur+1)
        save_one_page(ctt)

def save_one_page(content):
    entites = parse_ct2entity(content)
    session.add_all(entites)
    session.commit()

def run_pool():
    # index page
    ctt,_ = req_content(URL,'CN',1)
    #获得所有国家名字-简称
    ctry_key = parse_ct2option(ctt)
    #获取不同国家的vpn信息
    # for key in ctry_key:
    save_by_ctry_key('US')
    save_by_ctry_key('CN')

