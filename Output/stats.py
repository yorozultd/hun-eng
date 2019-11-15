import xml.etree.ElementTree as ET
import json

path =  './xmlDataSanitized.xml'
tree=ET.parse(path);
root = tree.getroot()

products =root.findall('product')
print("Total Number of Products : "+ str(len(products)))
stat={}
categories=0
for product in products: 
    if product.find('category') != None :
        if stat.get(product.find('category').text.strip()) == None :
            stat[product.find('category').text.strip()]=1   ;
            categories+=1;
        else :
            stat[product.find('category').text.strip()]=stat[product.find('category').text.strip()]+1

print("Total Number of Categories : "+ str(categories))
with open('result.json', 'w') as fp:
    json.dump(stat, fp)