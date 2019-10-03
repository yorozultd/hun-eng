import csv 
import xml.etree.ElementTree as ET

tree=ET.parse("../Output/xmlDataSanitized.xml")
root = tree.getroot()
with open('../Output/csvDataAll.csv', 'w') as writeFile:
    writer= csv.writer(writeFile)
    i=0
    for page in root : 
        i+=1
        try:
            sku= page.find("sku").text
            brand= page.find("brand").text
            price = page.find("price").text
            category= page.find("category").text
            writer.writerows([[sku,brand,price,category]])
        except :
            print(page.find("sku").text)