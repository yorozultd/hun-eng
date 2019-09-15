import csv 
import xml.etree.ElementTree as ET
import numpy as np 
dictionary= np.load("../Dictionary/dictionary.npy",allow_pickle=True)
products = ET.Element("products")
xmlDictionary={}
with open("csv_arak_ebrand_tulajs.csv") as f:
    field=1; 
    a=csv.reader(f)
    for i in a:
        if(len(i)>0 and i[0]!='|'):
            j=i[0]
            #print(i)
            data= j.split("|")
            if(len(data) <= 2):
                    print(data)
                    break
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
                j=i[1]
                fields = ET.SubElement(product, 'description')
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
mydata = ET.tostring(products)
myfile = open("../Output/xmlData.xml", "w")
myfile.write(mydata.decode('windows-1250'))
myfile.close()