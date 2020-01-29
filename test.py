import requests
from bs4 import BeautifulSoup as BS
import re
import csv

def toCSV(kakaku_list):
    file = open('kakaku_list.csv', 'w', encoding='ms932', newline='')
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

        if int(price_val) > 0:
            temp_list.append(["kakaku", maker + " " + title, price_val, price_kor])
 
    return temp_list

def dospara_Crawling(html, rate):
    temp_list = []
    title = None
    price = None
    price_val = 0
    tr_list = html.select('tr')

    for tr in tr_list :

        title_p = tr.find('td',{'ttl'})
        if title_p is not None:
            title = title_p.text

        price_p = tr.find('td',{'price'})
        if price_p is not None:
            price = price_p.text
        
        if title is not None and price is not None :
            p = re.compile("[0-9]")
            price_val = "".join(p.findall(price))
            if len(price_val) == 0:
                price_val = 0
            
            # 税込
            price_val = round(float(price_val)*1.1)
            price_kor = round(float(price_val)*rate)

            temp_list.append(["dospara", title, price_val, price_kor])
            title = None
            price = None

    return temp_list

def pckoubou_Crawling(html, rate):
    temp_list = []
    title = None
    price = None
    price_val = 0
    
    tr_list = html.select('div.container-item')
    
    for tr in tr_list :
        
        maker_p = tr.find('div',{'product-name'})
        if maker_p is not None:
            maker = maker_p.text.strip()
        
        title_p = tr.find('div',{'product-review fs16'}).find('a')
        if title_p is not None:
            title = title_p.text.strip()
        
        price_p = tr.find('div',{'price'})
        if price_p is not None:
            price = price_p.text

        p = re.compile("[0-9]")
        price_val = "".join(p.findall(price))
        if len(price_val) == 0:
            price_val = 0

        # 税込
        price_val = round(float(price_val)*1.1)
        price_kor = round(float(price_val)*rate)

        if int(price_val) > 0:
            temp_list.append(["pckoubou", maker + " " + title, price_val, price_kor])

    return temp_list

def danawa_Crawling(html, rate):
    temp_list = []
    title = None
    price = None
    price_val = 0

    tr_list = html.select('prod_item')


    return temp_list

#============================================================ 為替レート ============================================================#
rate = yen_Won_Rate()
#============================================================ kakaku ==================================================================#
kakaku_list = []

req = requests.get("https://kakaku.com/search_results/2070%20super/?category=0001%2C0028")

html = BS(req.text, 'html.parser')

kakaku_list += kakaku_Crawling(html,rate)
#============================================================ dospara =================================================================#
dospara_list = []
req2 = requests.get("https://www.dospara.co.jp/5shopping/search.php?ft=2070+super&search.x=0&search.y=0&search_for=category&sort=&bg=1&br=31&cate=bg1&sale_end=1")

html2 = BS(req2.text, 'html.parser')

dospara_list += dospara_Crawling(html2,rate)
#============================================================ pckoubou=================================================================#
pckoubou_list = []
req3 = requests.get("https://www.pc-koubou.jp/products/list.php?transactionid=07c16846017c7fdbd0cafa122323671f57d0f07f&mode=search&base_category_id=1905&spec1%5B%5D=GeForce+RTX+2070+SUPER")

html3 = BS(req3.text, 'html.parser')

pckoubou_list += pckoubou_Crawling(html3,rate)

#============================================================ danawa ===================================================================#
danawa_list = []
url = "http://search.danawa.com/dsearch.php?query=2070%20super&originalQuery=2070%20super&cate_c1=861&cate_c2=876&volumeType=allvs&page=1&limit=30&sort=saveDESC&list=list&boost=true&addDelivery=N&tab=main&tab=main"
req3 = requests.get(url)
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
result = BS(req3.text, 'lxml',headers=headers)
c = result.content
print(result.request.headers)


# danawa_list += danawa_Crawling(html4,rate)

#============================================================ all =====================================================================#

kakaku_list = kakaku_list + dospara_list + pckoubou_list

# toCSV(kakaku_list)


# for item in kakaku_list :
#     print(item)
