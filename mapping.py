import os
import requests
import json
import time
path = 'C:\\Users\\SY\\PycharmProjects\\tests\\Tables_Round1\\tables'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        #if '.txt' in file:
        files.append(os.path.join(r, file))

import urllib.parse
import pandas as pd
from datetime import datetime
d = {}
for f in files:
    df = pd.read_csv(f)

        # os.system('cls' if os.name == 'nt' else 'clear')
        # print (str(d))
        # with open("dict.txt", "w", encoding="utf8") as out_file:
        #     out_file.write(str(d))

    for i in range (0,df.shape[1]-1):
#    for i in range (0,df.shape[1]-1):
        type_dict = {}
        for j in range (0,len(df[df.keys()[0]])-1):
            col0 = df[df.keys()[0]][j]
            val = df[df.keys()[i+1]][j]

            try:
                val = datetime.strptime(val,"%d-%m-%y")
            except:
                pass
            typ = type(val)
            # d[typ] = val

            url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json&query="
            if typ is str:
                val = '"'+val+'"@en'
            elif typ is int or type is float:
                val = val
            elif typ is datetime:
                val = '"'+str(val.date())+'T00:00:00Z"^^xsd:dateTime'

            query = 'SELECT * ' \
                    'WHERE ' \
                    '{' \
                    ' ?s ?p "' + str(col0) +'"@en .' \
                    '  ?s ?p2 ?o.' \
                    ' ?o ?p3 '+str(val) +'.' \
                    '}'

            query_encoded = urllib.parse.quote(query)

            x = requests.get(url+query_encoded)
            content = x.content.decode("UTF8").replace("\n","").replace("\t","")
            time.sleep(1)
            try:
                res = json.loads(content)
                pred = res["results"]["bindings"][0]["p2"]["value"]
            except:
                pred = ""
            if pred is not "":
                type_dict[pred] = 1
        if len(type_dict)>1:
            print ("conflict")
            pred_temp =""
            for item in type_dict.items():
                if pred_temp is not "":
                    pred_temp = pred_temp + ","+item[0]
                else:
                    pred_temp = item[0]

        elif len(type_dict)==1:
            for item in type_dict.items():
                pred_temp = item[0]
            # for item in type_dict.items():
            #     pred = pred + ","+item[0]
        elif len(type_dict)==0:
            pred = ""

        file_name = f.split("\\")[len(f.split("\\"))-1].split(".")[0]
        with open("out.txt", "a") as out_file:
            write_str = '"'+file_name +'"'+ '"'+",0"+'"'+","+'"'+str(i+1)+'"'+","+'"'+pred+'"'+'\n'
            print(write_str)
            out_file.write(write_str)
