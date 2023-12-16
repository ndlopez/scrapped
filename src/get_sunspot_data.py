'''
   Download csv file from SIDC site,
   Read local csv file and edit date to output w/better format
   source: https://sidc.be/SILSO/datafiles
'''
from urllib.request import urlretrieve
import csv

csv_url = "https://sidc.be/silso/DATA/SN_d_tot_V2.0.csv"

path_file = "../../../Downloads/SN_d_tot_V2.0.csv"
print("Downloading...")
path,headers = urlretrieve(csv_url,path_file)
for name, val in headers.items():
   print(name,val)

print("Processing file...",path_file)
newFile = []
fields = ["date","spotNum"]
startYear = 2007

with open(path_file,mode="r") as data_file:
    csvFile = csv.reader(data_file,delimiter=";")
    auxArr = ""
    for lines in csvFile:
        if not lines[0] == "year":
            if int(lines[0]) > startYear:
                newArr = []
                auxArr = lines[0] + "-" + lines[1] + "-" + lines[2]
                # my_data = dict(date = auxArr,value = lines[4].strip())
                newArr.append(auxArr)
                newArr.append(lines[4].strip())
                newFile.append(newArr)


outFile = "../data/sunspot_number2.csv"
with open(outFile,"w",newline='') as new_file:
    write = csv.writer(new_file)
    write.writerow(fields)
    write.writerows(newFile)
print("done.")
