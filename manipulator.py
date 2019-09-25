# Swisstimeshop project 2019 -- written by Bence Ladoczki info@ldczk.com
# Upload the watches to no1brand.ru
# Usage: python3 manipulator.py

import requests
import xml.etree.ElementTree as ET
import json
import sys
import csv

print("Launching application...")

category_translator = {'Okosóra': 'Smartwatch'}

allowed_categories = ["womanly okosóra","womanly wristwatch","womanly okosóra","Okosóra"]

add_product_endpoint = "http://no1brand.ru/add-product/"

input_xml = "Output/xmlDataAll.xml"
tree = ET.parse(input_xml)
root = tree.getroot()

products_from_file = [x for x in root.findall('./product')]

print("Found ("+str(len(products_from_file))+") products...")

categories_from_file = [[x.findall("category")[0].text,x.findall("sku")[0].text] for x in products_from_file if len(x.findall("category")) > 0]
categories = [x[0] for x in categories_from_file]
unqiue_categories = set(categories)

print(str(unqiue_categories))

allowed_products = [x for x in products_from_file if len(x.findall("category")) > 0 and len(x.findall("description")) > 0 and x.findall("category")[0].text in allowed_categories]

print("Found ("+str(len(allowed_products))+") allowed products...")

for product in allowed_products:

 sku   = product.findall("sku")[0].text if len(product.findall("sku")) > 0 else "UNKNOWN"
 brand = product.findall("brand")[0].text if len(product.findall("brand")) > 0 else "UNKNOWN"
 title = brand + " - " + sku
 
 novat_price = product.findall("price")[0].text if len(product.findall("price")) > 0 else "UNKNOWN"
 street_price = str(float(novat_price) * 1.5)
 suggested_price = novat_price
 
 image_1 = product.findall("image")[0].text if len(product.findall("image")) > 0 else "UNKNOWN"
 image_2 = ""
 image_3 = ""
 
 category = product.findall("category")[0].text if len(product.findall("category")) > 0 else "UNKNOWN"
 category = category_translator[category] if category in category_translator.keys() else category
 
 supplier = "swisstime"
 
 description = product.findall("description")[0].text if len(product.findall("description")) > 0 else "UNKNOWN"
 
 titleInEnglishFromFeed = title
 
 english_category = category
 
 stock_info = 1
 
 style = "UNKNOWN"
 colour = "UNKNOWN"
 gender = "UNKNOWN"
 extended_description = description+"_1"
 descriptionInEnglishFromFeed = description+"_1"
 english_style = "UNKNOWN"
 
 print("Now at: "+str(title))
 
 payload = {
               'description':                      description,
               'extended_description':             extended_description,
               'descriptionInEnglishFromFeed':     descriptionInEnglishFromFeed,
               'titleInEnglishFromFeed':           titleInEnglishFromFeed,
               'english_category':                 english_category,
               'english_style':                    english_style,
               'title':                            title,
               'sku':                              sku,
               'stock_info':                       stock_info,
               'supplier':                         supplier,
               'brand':                            brand,
               'image_1':                          image_1,
               'category':                         category,
               'style':                            style,
               'colour':                           colour,
               'gender':                           gender,
               'image_2':                          image_2,
               'image_3':                          image_3,
               'street_price':                     street_price,
               'suggested_price':                  suggested_price,
               'novat_price':                      novat_price
              }
 r = requests.post(add_product_endpoint, data=payload)
 print(r.text)
