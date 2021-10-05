import os
import requests
import json
import time
import csv
import urllib.parse
import pandas as pd
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
if os.name == "nt":
    print("OS "+os.name)
    path = 'C:\\Users\\SY\\Google Drive\\PRIVATE MATERIAL\\semtab2020\\Tables_Round1\\tables\\'
else:
    print("OS "+os.name)
    path = '/tables/'

with open("CPA_Round1_Targets.csv", 'r') as csvfile:
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
                for j in range (0,len(df[df.keys()[0]])-1):
                    col0 = df[df.keys()[0]][j]
                    val = df[df.keys()[int(row[2])]][j]

                    try:
                        val = datetime.strptime(val,"%Y-%m-%d")
                    except:
                        pass
                    typ = type(val)
                    # d[typ] = val
                    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

                    # url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json&query="
                    if typ is str:
                        val = "'"+val+"'"+"@en"
                    elif typ is int or type is float:
                        val = val
                    elif typ is datetime:
                        val = "'"+str(val.date())+"T00:00:00Z"+"'"+"^^xsd:dateTime"

                    sparql.setQuery("SELECT * " +
                            "WHERE " +
                            "{" +
                            " ?s rdfs:label "+"'" + str(col0) +"'"+"@en ." \
                            "  ?s ?p2 ?o." \
                            " ?o ?p3 "+str(val) +"." \
                            "}")
                    sparql.setReturnFormat(JSON)
                    results = sparql.query().convert()
                    #
                    # query = 'SELECT * ' \
                    #         'WHERE ' \
                    #         '{' \
                    #         ' ?s rdfs:label "' + str(col0) +'"@en .' \
                    #         '  ?s ?p2 ?o.' \
                    #         ' ?o ?p3 '+str(val) +'.' \
                    #         '}'

                    # query_encoded = urllib.parse.quote(query)

                    # x = requests.get(url+query_encoded)
                    # content = x.content.decode("UTF8").replace("\n","").replace("\t","")
                    # time.sleep(0.1)
                    try:
                        sparql.setReturnFormat(JSON)
                        res = sparql.query().convert()
                        # res = json.loads(content)
                        # pred = res["results"]["bindings"][0]["p2"]["value"]
                        for bind in res["results"]["bindings"]:
                            pred = bind["p2"]["value"]
                            if pred in type_dict:
                                type_dict[pred] +=1
                            else:
                                type_dict[pred] = 1
                    except:
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