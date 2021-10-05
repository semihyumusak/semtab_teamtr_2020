import os
import requests
import json
import time
import csv
import urllib.parse
import pandas as pd
from datetime import datetime

if os.name == "nt":
    print("OS "+os.name)
    path = 'C:\\Users\\semih.yumusak\\Google Drive\\makaleler\\semtab2020\\tables\\'
    # path = 'C:\\Users\\SY\\Google Drive\\PRIVATE MATERIAL\\semtab2020\\Tables_Round1\\tables\\'
else:
    print("OS "+os.name)
    path = '/tables/'

with open("CPA_Round1_Targets_After80K.csv", 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        try:
            try:
                with open("out.csv", "r") as existing:
                    out_str = existing.read()
            except:
                out_str=""
            if str(row).replace("[","").replace("]","")+"," in out_str:
                pass
            else:
                df = pd.read_csv(path+row[0]+".csv")

                    # os.system('cls' if os.name == 'nt' else 'clear')
                    # print (str(d))
                    # with open("dict.txt", "w", encoding="utf8") as out_file:
                    #     out_file.write(str(d))

                type_dict = {}
                brk =0
                for j in range (0,len(df[df.keys()[0]])-1):
                    if brk ==1:
                        break
                    brk = 0
                    col0 = df[df.keys()[0]][j]
                    val = df[df.keys()[int(row[2])]][j]

                    try:
                        val = datetime.strptime(val,"%Y-%m-%d")
                    except:
                        pass
                    try:
                        if "." in val:
                            val = float(val)
                    except:
                        pass
                    try:
                        if "." not in val:
                            val = int(val)
                    except:
                        pass
                    typ = type(val)
                    # d[typ] = val

                    url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json&query="
                    if typ is str:
                        val = '"'+val+'"@en'
                    elif typ is int:
                        val = '"'+str(val)+'"^^xsd:integer'
                    elif type is float:
                        val = '"'+str(val)+'"^^xsd:decimal'
                    elif typ is datetime:
                        val = '"'+str(val.date())+'T00:00:00Z"^^xsd:dateTime'

                    query = 'SELECT * ' \
                            'WHERE ' \
                            '{' \
                            ' ?s rdfs:label "' + str(col0) +'"@en .' \
                            '  ?s ?p2 ?o.' \
                            ' ?o ?p3 '+str(val) +'.' \
                            '}'

                    query_encoded = urllib.parse.quote(query)
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

                    time.sleep(0.2)
                    try:
                        x = requests.get(url + query_encoded, headers=headers, timeout=10)
                        content = x.content.decode("UTF8").replace("\n", "").replace("\t", "")

                        res = json.loads(content)
                        # pred = res["results"]["bindings"][0]["p2"]["value"]
                        for bind in res["results"]["bindings"]:
                            pred = bind["p2"]["value"]
                            if pred in type_dict:
                                type_dict[pred] +=1
                                if type_dict[pred]==3 and len(type_dict)==1:
                                    brk = 1
                            else:
                                type_dict[pred] = 1
                    except BaseException as b:
                        print (b)
                        pred = ""

                if len(type_dict)>1:
                    print ("conflict")
                    pred_temp =""
                    max = -1
                    for item in type_dict.items():
                        if max < int(item[1]):
                            max = int(item[1])
                            max_pred = item[0]
                    row.append(max_pred)
                    row.append(max)
                    for item in type_dict.items():
                        row.append(item[0])
                        row.append(item[1])


                elif len(type_dict)==1:
                    for item in type_dict.items():
                        row.append(item[0])

                elif len(type_dict)==0:
                    pred = ""

                with open("out.csv", "a") as out_file:
                    write_str = str(row).replace("[","").replace("]","")
                    print(write_str)
                    out_file.write(write_str+"\n")
        except BaseException as b:
            print ("ana hata" + str(b))