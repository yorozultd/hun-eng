import csv 
import xml.etree.ElementTree as ET
import numpy as np 
import requests
from contextlib import closing
import pycurl

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
dictionary= np.load("../Dictionary/dictionary.npy",allow_pickle=True)
products = ET.Element("products")
xmlDictionary={}        
  
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
                sku=True
                new=True
            else :
                product=xmlDictionary.get(data[0].strip())
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
                        fields = ET.SubElement(product, 'field_'+data[1])
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
                        else :
                            fields.text =  k;
                    else :
                        fields.text =dictionary.item().get(k.lower().strip())[0]
            if(len(i)==2):  
                k=i[1]
                fields = ET.SubElement(product, 'description')
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
                        fields.text= str(" ".join(K)).strip()
                    else :
                        fields.text =  k;
                else :
                    fields.text =dictionary.item().get(k.lower().strip())[0]
mydata = ET.tostring(products)
myfile = open("../Output/xmlData.xml", "w")
myfile.write(mydata.decode('windows-1250'))
myfile.close()
