"""
    Write json file every time this app is called
"""
import json

down_data = {}

down_data["consult_time"] = "2023-08-06 20:39:43"
down_data["request_date"] = "2023/07/27"
pdf_array = []
aux_dic = {}
aux_dic["title"] ="Television Room - Engines Are Starting"
aux_dic["link"]="https://cdn-albums.tunein.com/gn/NJ4KL637GTg.jpg"
pdf_array.append(aux_dic)
down_data["downloaded"] = pdf_array

outfile = r"down_data.json"
with open(outfile,"w",encoding='utf8') as fp:
    json.dump(down_data,fp,indent=4)
