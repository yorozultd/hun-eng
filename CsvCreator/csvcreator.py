import csv 
import xml.etree.ElementTree as ET

tree=ET.parse("../Output/xmlDataAll.xml")
root = tree.getroot()
with open('../Output/csvDataAll.csv', 'w') as writeFile:
    writer= csv.writer(writeFile)
    i=0
    for page in root : 
        i+=1
        try:
            sku= page.findall("sku")[0].text
            print(sku)
            brand= page.findall("brand")[0].text
            price = page.findall("price")[0].text
            category= page.findall("category")[0].text
            writer.writerows([[sku,brand,price,category]])
        except :
            print(page.find("sku").text)