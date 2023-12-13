#!/usr/bin/python3
'''
   Moon Rise/Set times, distance to Earth, % illumination
   extracting data from www.timeanddate.com
   https://gist.github.com/tk87s
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
    source=urlopen(my_url)
    print("Access granted")
except HTTPError as err:
    # does not work :(
    print("Access denied or...", err.code)
    print("Better use curl to fetch the page...")
    source = open('MoonriseSet_Nagoya.htm','r',encoding="cp932")

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
            if "月" in str(aux):
                aux = str(aux).replace("月","")
            if aux is None:
                aux = jdx - 1
            
            aux2 = monty
            if int(monty) < 10:
                aux2 = "0" + aux2
            # print(f"{year}-{aux2}-{aux}",end=';')
            # should skip 1st line
            # aux if int(aux) > 10 else "0"+str(aux)
            zoeyArr.append(f"{year}-{aux2}-{aux}")
            for idx in range(len(tab_td)):
                if tab_td[idx].string == "-":
                    val_ery = tab_td[0].string
                else:
                    val_ery = tab_td[idx].string                
                zoeyArr.append(str(val_ery))
                # print(type(str(val_ery)) ,end=';')

            """for td_item in tab_td:
                print(td_item.string,end=',')"""
            # print()
            newFile.append(zoeyArr)
        jdx += 1


get_info("tb-7dmn")

zoeyArr = []
aux = ("時","分","%",",")

for item in newFile:
    fields = []
    for elem in item:
        print(elem,end=";")
        # if "時" in elem:
        #    elem = elem.replace("時", ":")
        for el in aux:
            if el in elem:
                elem = elem.replace(el, "")
        fields.append(elem)
    zoeyArr.append(fields)

outFile = "../data/moon.csv"
# outFile = "moonthy.csv"

with open(outFile,"w",newline='') as new_file:
    write = csv.writer(new_file)
    write.writerows(zoeyArr)
 
#print(zoeyArr)
"""sample output
2023-09-9月;Moonrise;Moonset;Moonrise;Distance (km);Illumination;
2023-09-1;-;6時20分;19時16分;358,124;99.4%;
"""
