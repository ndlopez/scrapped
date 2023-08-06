import json

down_data = {}

down_data["consult_time"] = "2023-08-06 20:39:43"
down_data["request_date"] = "2023/07/27"
pdf_array = []
down_data["downloaded"] = pdf_array

outfile = r"down_data.json"
with open(outfile,"a",encoding='utf8') as fp:
    json.dump(down_data,fp,indent=4)


