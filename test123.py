from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen
# import urllib.request as urllib2

url="http://www.conakat.com/states/ohio/cities/defiance/road_maps/"

html = urlopen(url)

soup = BeautifulSoup(html, "html.parser")

f = csv.writer(open("Defiance Steets1.csv", "w"))
f.writerow(["Name", "ZipCodes"]) # Write column headers as the first line

links = soup.find_all('a')

for link in links:
    i = link.find_next_sibling('i')
    if getattr(i, 'name', None):
        a, i = link.string, i.string
        f.writerow([a, i])