#!/usr/bin/python3
''' 
   Moon Rise/Set times, distance to Earth, % illumination
   extracting data from www.timeanddate.com
'''
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import sys,csv

if len(sys.argv) <= 2:
    print("A valid year and month are required: YYYY MM")
    sys.exit()

year = sys.argv[1] #year "2023"
monty = sys.argv[2] #monty "8"
location = "nagoya"

my_url=f"https://www.timeanddate.com/moon/japan/{location}?month={monty}&year={year}"

try:
    #when downloading a page...
    source=urlopen(my_url)
    print("Access granted")
except HTTPError as err:
    print("Access denied or...", err.code)
    print("Better use curl to fetch the page...")
    source = open('../../../MoonTimes.html','r')

soup = BeautifulSoup(source.read(),'html.parser')
fields = []
newFile = []
def get_info(tab_id):
    tables = soup.find('table',id=tab_id)
    tab_tr = tables.find_all('tr')
    jdx=0
    for item in tab_tr:
        tab_th = item.find('th')
        tab_td = item.find_all(class_='sep') #pdr0
        if tab_th is not None and jdx > 0:
            zoeyArr = []
            aux = tab_th.string
            if aux is None:
                aux = jdx - 1
            aux2 = monty
            if int(monty) < 10:
                aux2 = "0" + aux2
            print(f"{year}-{aux2}-{aux}",end=';')
            zoeyArr.append(f"{year}-{aux2}-{aux}")
            for idx in range(len(tab_td)):
                if tab_td[idx].string == "-":
                    val_ery = tab_td[0].string
                else:
                    val_ery = tab_td[idx].string
                print(val_ery,end=';')
                zoeyArr.append(val_ery)
            """for td_item in tab_td:
                print(td_item.string,end=',')"""
            print()
            newFile.append(zoeyArr)
        jdx += 1

get_info("tb-7dmn")

"""outFile = "../data/moon.csv"
with open(outFile,"w",newline='') as new_file:
    write = csv.writer(new_file)
    write.writerow(fields)
    write.writerows(newFile)
"""
# print(newFile)
newArr = []
for item in newFile:
   zoeyArr = []
   for elem in item:
      x = elem.find(",")
      print(type(elem))
      # only date is string, the other elems are <class 'bs4.element.NavigableString'>
      if x:
         #print("found comma")
         elem.replace(",",":")
      zoeyArr.append(elem)
   newArr.append(zoeyArr)

print(newArr)
"""sample output
2023-09-9月;Moonrise;Moonset;Moonrise;Distance (km);Illumination;
2023-09-1;-;6時20分;19時16分;358,124;99.4%;
"""

