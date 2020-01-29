import requests
from bs4 import BeautifulSoup as BS
import re
import csv

def toCSV(kakaku_list):
    file = open('kakaku_list.csv', 'w', encoding='utf-8', newline='')
    csvfile = csv.writer(file)
    for row in kakaku_list :
        csvfile.writerow(row)
    file.close()

def yen_Won_Rate():

    rate_list = []
    req = requests.get("https://ko.exchange-rates.org/Rate/JPY/KRW")

    html = BS(req.text, 'html.parser')

    rate_list = html.findAll('td',{'text-nowrap text-narrow-screen-wrap'})

    rate = float(rate_list[1].text.strip(' KRW'))

    return rate

def kakaku_Crawling(html, rate):
    temp_list = []
    title = None
    price_val = 0

    tr_list = html.select('div.p-result_item_row')
 
    for tr in tr_list :

        maker_p = tr.find('p',{'p-item_maker'})
        if maker_p is not None:
            maker = maker_p.text

        title_p = tr.find('p',{'p-item_name s-biggerlinkHover_underline'})
        if title_p is not None:
            title = title_p.text

        price_p = tr.find('span',{'c-num p-item_price_num'})
        if price_p is not None:
            price = price_p.text
            p = re.compile("[0-9]")
            price_val = "".join(p.findall(price))
            if len(price_val) == 0:
                price_val = 0
            
            price_kor = round(float(price_val)*rate)

        if title is not None:
            temp_list.append([maker, title, price_val, price_kor])
 
 
    return temp_list
#============================================================ End of mnet_Crawling() ============================================================#

kakaku_list = []

rate = yen_Won_Rate()

req = requests.get("https://kakaku.com/search_results/2070%20super/?category=0001%2C0028")

html = BS(req.text, 'html.parser')

kakaku_list += kakaku_Crawling(html,rate)

toCSV(kakaku_list)
# for item in kakaku_list :
#     print(item)
