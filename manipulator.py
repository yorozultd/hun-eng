# Swisstimeshop project 2019 -- written by Bence Ladoczki info@ldczk.com
# Upload the watches to no1brand.ru
# Usage: python3 manipulator.py

import requests
import xml.etree.ElementTree as ET
import json
import sys
import csv

#######################################################################################################
class XmlParser:
 def __init__(self):
  self.root = None
 def set_root(self,root):
  self.root = root
 def return_field(self,field_name):
  return self.root.findall(field_name)[0].text if len(self.root.findall(field_name)) > 0 else "UNKNOWN"
#######################################################################################################
# Entry #
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

xp = XmlParser()
counter = 1
for product in allowed_products:

 if(counter == 2):
  sys.exit(1)

 xp.set_root(product)

 sku   = xp.return_field("sku")
 brand = xp.return_field("brand")
 title = brand + " - " + sku
 
 novat_price = xp.return_field("price")
 street_price = str(float(novat_price) * 1.5)
 suggested_price = novat_price
 
 image_1 = xp.return_field("image")
 image_2 = ""
 image_3 = ""
 
 category = xp.return_field("category")
 category = category_translator[category] if category in category_translator.keys() else category
 
 supplier = "swisstime"
 
# description = xp.return_field("description")

 diameter       =  xp.return_field("atmero")
 case_height    =  xp.return_field("tok_magassag")
 case_thickness =  xp.return_field("tok_vastagsag")
 waterproof     =  xp.return_field("vizallosag")
 strap_width    =  xp.return_field("szij_szelesseg")
 strap_width    =  xp.return_field("szij_szelesseg")
 description = "While the history and precision timekeeping offered by "+brand+" watches is appealing, today, this is one of the most well-known brands around the globe. A showcase of quality and modern design, our "+brand+" collection delivers elegance and sophistication to suit any occasion. our company provides access to years of "+brand+" models, specializing in only like-new options, to ensure you receive the exquisite timepiece you expect. <br> "
 description += "Diameter: "+diameter + "<br>"
 description += "Case height: "+case_height + "<br>"
 description += "Case thickness: "+case_thickness + "<br>"
 description += "Waterproof: "+waterproof + "<br>"
 description += "Strap width: "+strap_width + "<br><br>"
 description += "Any questions? Do not hesitate to send us a message and we will answer your questions in a prompt manner!"
 
 titleInEnglishFromFeed = title
 
 english_category = category
 
 stock_info = 1
 
 style = "UNKNOWN"
 colour = "UNKNOWN"
 gender = "UNKNOWN"
 extended_description = description+"_1"
 descriptionInEnglishFromFeed = description+"_1"
 english_style = "UNKNOWN"
 
 print("Now at: "+str(title)+" ("+str(counter)+"/"+str(len(allowed_products))+")")
 
 payload = {
               'swiss_description':                description,
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
 counter += 1
