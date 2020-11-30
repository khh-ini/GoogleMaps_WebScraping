import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import time

data_pusat_kesehatan = []

data_file = ['klinik.html','rumahsakit.html','rumahsakit2.html']

for rs in data_file : 
    rs = open('klinik.html', 'r')
    # page = requests.get('https://www.google.com/maps/search/Rumah+Sakit/@0.4954942,101.4484785,13z')
    soup = BeautifulSoup(rs.read(), 'html.parser')

    elemen_rs = soup.find_all('div',class_='uMdZh tIxNaf mnr-c')

    for e in elemen_rs: 
        data_rs = {
            'nama_rs': None,
            'rating_rs': None,
            'jenis_rs': None,
            'alamat_rs': None,
            'koordinat_rs': None
        }
        nama_rs = e.find('div', class_='dbg0pd')
        rating_rs = e.find('span', class_='rllt__details lqhpac').find('span', class_='BTtC6e')
        jenis_rs = e.find('span', class_='rllt__details lqhpac').find('div')
        alamat_rs = e.find('span', class_='rllt__details lqhpac').find('span', attrs={'class':None, 'style':None, 'aria-label':None})

        if( nama_rs is not None):
            data_rs['nama_rs'] = nama_rs.text
        if( rating_rs is not None):
            data_rs['rating_rs'] = rating_rs.text
        if( jenis_rs is not None):
            data_rs['jenis_rs'] = jenis_rs.text.split(' · ')[-1]
        if(alamat_rs is not None): 
            data_rs['alamat_rs'] = alamat_rs.text
        if(e.find('a', class_='yYlJEf VByer') is None):
            continue
        maps_url = 'https://www.google.com'+e.find('a', class_='yYlJEf VByer')['data-url']
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0','referer':'https://www.google.com/'}
        coordinat = parse_qs(urlparse(BeautifulSoup(requests.get(maps_url).text, 'html.parser').find('meta', attrs={'itemprop':'image'})['content']).query)['markers']
        data_rs['koordinat_rs'] = coordinat
        print(data_rs)
        data_pusat_kesehatan.append(data_rs)
        time.sleep(3)


    try :
        with open('datatest.csv','w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['nama_rs','rating_rs','jenis_rs','alamat_rs','koordinat_rs'])
            writer.writeheader()
            for data in data_pusat_kesehatan :
                writer.writerow(data)

    except IOError : 
        print("I/O Error")

