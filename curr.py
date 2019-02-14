
import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import OrderedDict
from datetime import date

classes = ['currency-name-container', 'col-symbol', 'market-cap']
domain = 'https://coinmarketcap.com'
url = '{}/all/views/all/'.format(domain)

def get_field(curr, cls):
    return curr.find('a', class_=cls).text

def get_html(url):
    return requests.get(url).text

def get_all_rows(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.find('table', id='currencies-all').find('tbody').find_all('tr')

currencies_all = []
for curr in get_all_rows(get_html(url)):
    # import pdb; pdb.set_trace()
    currencies_all.append([
        curr.find('a', class_='currency-name-container').text,
        '{}{}'.format(domain, curr.find('a', class_='currency-name-container')['href']),
        curr.find('td', class_='col-symbol').text,
        curr.find('td', class_='market-cap').text,
        curr.find('a', class_='price').text,
        '{}{}'.format(domain, curr.find('a', class_='price')['href']),
        curr.find('td', class_='circulating-supply').text,
        curr.find('a', class_='volume').text,
        '{}{}'.format(domain, curr.find('a', class_='volume')['href']),
        curr.find('td', class_='percent-change', attrs={"data-timespan":"1h"}),
        curr.find('td', class_='percent-change', attrs={"data-timespan":"24h"}),
        curr.find('td', class_='percent-change', attrs={"data-timespan":"7d"}),
        ])


labels = [
'name',
'path',
'alias',
'capitalization',
'price/usd',
'price url',
'circualting',
'amount',
'amaunt url',
'1h',
'24h',
'7d',
]
df = pd.DataFrame.from_records(currencies_all, columns=labels)
