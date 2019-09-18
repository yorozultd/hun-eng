import csv 
import xml.etree.ElementTree as ET
import numpy as np 
import requests
from contextlib import closing
import pycurl
dictionary= np.load("../Dictionary/dictionary.npy",allow_pickle=True)

url = 'https://swisstimeshop.hu/feeds/csv_arak_ebrand_tulajs.csv'
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}
products = ET.Element("products")
xmlDictionary={}  
pager={}  
converter = {} 
with open("fields.csv") as f:                 #  offline  
    a=csv.reader(f)                                           # offline
    for i in a: 
        converter[int(i[0])] = i[1];     

r = requests.get(url,headers=headers) 
  
with open("download.csv",'wb') as f: 
    f.write(r.content) 

with open("download.csv") as f:                 #  offline  
    field=1; 
    debug =0
    a=csv.reader(f)                                           # offline
    for i in a:
        if(len(i)>0 and i[0]!='|'):
            j=i[0]
            #print(i)
            data= j.split("|")
            if(len(data) <= 2):
                    print(data)
                    continue
           
            if(xmlDictionary.get(data[0].strip())==None):
                product = ET.SubElement(products, 'product')
                xmlDictionary[data[0].strip()]=product
                pager[data[0].strip()]=int(data[1])
                sku=True
                new=True
            else :
                product=xmlDictionary.get(data[0].strip())
                pager[data[0].strip()]=int(data[1])
                sku=False
                new=False
            for k in data : 
                if not new : 
                    new=True
                    continue
                if k==data[1]:
                    continue
                
                if(k!=''):
                    if not sku :
                        if int(data[1]) > 0 and int(data[1]) < 43:
                            fields = ET.SubElement(product,converter[int(data[1])])
                        else :
                            fields = ET.SubElement(product,'field_'+data[1])
                        tempF=fields
                    else :
                        fields = ET.SubElement(product, 'sku')
                        sku=False
                    if(dictionary.item().get(k.lower().strip())==None):
                        if(len(k.strip().split(' '))>1 ):
                            K=k.strip().split(" ")
                            k=k.strip()
                            for l in range(len(K)):
                                if(dictionary.item().get(K[l].lower().strip())==None):
                                    pass
                                else: 
                                    K[l]=dictionary.item().get(K[l].lower().strip())[0]
                            fields.text= str(" ".join(K)).strip()
                            temp= str(" ".join(K)).strip()
                        else :
                            fields.text =  k;
                            temp =  k;
                    else :
                        fields.text =dictionary.item().get(k.lower().strip())[0]
                        temp =dictionary.item().get(k.lower().strip())[0]
                        
            if(len(i)==2):  
                k=i[1]
                #fields = ET.SubElement(product, 'field_'+data[1])
                fields=tempF
                k="".join(k.split("|")).strip()
                if(dictionary.item().get(k.lower().strip())==None):
                    if(len(k.strip().split(' '))>1 ):
                        K=k.strip().split(" ")
                        k=k.strip()
                        for l in range(len(K)):
                            if(dictionary.item().get(K[l].lower().strip())==None):
                                pass
                            else: 
                                K[l]=dictionary.item().get(K[l].lower().strip())[0]
                        fields.text=temp+ str(" ".join(K)).strip()
                    else :
                        fields.text =temp+  k;
                else :
                    fields.text =temp +dictionary.item().get(k.lower().strip())[0]





url = 'https://swisstimeshop.hu/feeds/csv_arak_ebrand.csv'
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


#xmlDictionary={}        
  
r = requests.get(url,headers=headers) 
  
with open("download1.csv",'wb') as f: 
    f.write(r.content) 



with open("download1.csv") as f:                 #  offline  
    field=1; 
    debug =0
    a=csv.reader(f)                                           # offline
    
    for i in a:
        debug=0
        counter=0
        if(len(i)>0 and i[0]!='|'):
            for j in i :
                counter+=1
            #print(i)
                if debug ==0 : 
                    if(len(i)< 2):
                        print(i)
                        break
                    else :
                        heading = i[1].split("|")[0]
                    if(xmlDictionary.get(heading.split(" ")[-1].strip())==None):
                        product = ET.SubElement(products, 'product')
                        xmlDictionary[heading.strip()]=product
                        sku=True
                        new=True
                        fields = ET.SubElement(product, 'sku')
                        fields.text= heading.strip()
                        fielddata=0
                    else :
                        product=xmlDictionary.get(heading.split(" ")[-1].strip())
                        sku=False
                        new=False
                        fields = ET.SubElement(product, 'title')
                        fields.text= heading.strip()
                        fielddata=pager[heading.split(" ")[-1].strip()]
                    debug+=1
                
                data= j.split("|")
                for datas in data:
                    fielddata+=1
                    pager[heading.split(" ")[-1].strip()]=fielddata
                    if counter==2:
                        counter=3
                        continue
                    if datas!='': 
                        if fielddata < 43:
                            fields = ET.SubElement(product, converter[fielddata])
                        else:
                            fields = ET.SubElement(product, "field_"+str(fielddata))
                        tempF=fields
                        fielddata+=1
                        if(dictionary.item().get(datas.lower().strip())==None):
                            if(len(datas.strip().split(' '))>1 ):
                                K=datas.strip().split(" ")
                                datas=datas.strip()
                                for l in range(len(K)):
                                    if(dictionary.item().get(K[l].lower().strip())==None):
                                        pass
                                    else: 
                                        K[l]=dictionary.item().get(K[l].lower().strip())[0]
                                fields.text= str(" ".join(K)).strip()
                            else :
                                fields.text =  datas;
                        else :
                            fields.text =dictionary.item().get(datas.lower().strip())[0]
            
        







mydata = ET.tostring(products)
myfile = open("../Output/xmlDataAll.xml", "w")
myfile.write(mydata.decode('windows-1250'))
myfile.close()
