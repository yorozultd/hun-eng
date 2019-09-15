import csv 
import xml.etree.ElementTree as ET
import numpy as np 
dictionary= np.load("../Dictionary/dictionary.npy",allow_pickle=True)
products = ET.Element("products")
with open("csv_arak_ebrand_tulajs.csv") as f:
    field=1; 
    a=csv.reader(f)
    for i in a:
        product = ET.SubElement(products, 'product')
        for j in i  :
            data= j.split("|")
            for k in data : 
                if(k!=''):
                    fields = ET.SubElement(product, 'field_'+str(field))
                    if(dictionary.item().get(k.lower())==None):
                        fields.text =  k;
                    else :
                        fields.text =dictionary.item().get(k.lower())[0]
                    field+=1
mydata = ET.tostring(products)
myfile = open("../Output/xmlData.xml", "w")
myfile.write(str(mydata))
myfile.close()
