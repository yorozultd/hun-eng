import csv 
import xml.etree.ElementTree as ET
import numpy as np 
import requests
from contextlib import closing
dictionary= np.load("../Dictionary/dictionary.npy",allow_pickle=True)


class SwisstimeXML: 
    def __init__(self):
        pass
    def download_data(self,output_csv_filename_1,output_csv_filename_2):
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
        r = requests.get(url,headers=headers) 
        with open(output_csv_filename_1+".csv",'wb') as f:  #download
            f.write(r.content) 
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
        with open(output_csv_filename_2+".csv",'wb') as f:  #download1
            f.write(r.content) 
    def process_data(self):
        products = ET.Element("products")
        xmlDictionary={}  
        pager={}  
        converter = {} 
        with open("fields.csv") as f:                 #  offline  
            a=csv.reader(f)                                           # offline
            for i in a: 
                converter[int(i[0])] = i[1];     



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







        fieldIndex=0
        descriptionMapper={}
        descriptionField={}
        fieldsdata = ['type','brand','category','price','image','link','price_2','price_3','sku','size_1','size_2','size_3','category_2','data_1','data_2','data_3']#,'description']
        with open("download1.csv") as f:                 #  offline  
            field=1; 
            debug =0
            a=csv.reader(f)                                           # offline

            for i in a:
                debug=0
                counter=0
                if(len(i)>0 and i[0]!='|') or True:
                    for j in i :
                        counter+=1
                    #print(i)
                        if debug ==0 : 
                            if(len(i)< 2):
                                print(i)
                                break
                            else :
                                heading = i[1].split("|")[0]
                                try: 
                                    heading2= i[1].split("|")[7].strip()
                                except: 
                                    heading2=None
                            if(xmlDictionary.get(heading.split(" ")[-1].strip())==None):
                                if(xmlDictionary.get(heading2)==None):
                                    product = ET.SubElement(products, 'product')
                                    xmlDictionary[heading.strip()]=product
                                    sku=True
                                    new=True
                                    fields.text= heading.strip()
                                    fielddata=0
                                    fieldIndex=0
                                    fields = ET.SubElement(product, 'sku')
                                else :
                                    product=xmlDictionary.get(heading2)
                                    sku=False
                                    new=False
                                    fields = ET.SubElement(product, 'title')
                                    fields.text= heading.strip()
                                    fieldIndex=0
                                    #fielddata=pager[heading.split(" ")[-1].strip()]
                                    fielddata=0

                            else :
                                product=xmlDictionary.get(heading.split(" ")[-1].strip())
                                sku=False
                                new=False
                                fields = ET.SubElement(product, 'title')
                                fields.text= heading.strip()
                                fieldIndex=0
                                #fielddata=pager[heading.split(" ")[-1].strip()]
                                fielddata=0
                            debug+=1

                        data= j.split("|")
                        #data = [x for x in data if x != '']
                        print(data)


                        diss =False
                        datas=-1
                        while datas < len(data)-1:
                            datas+=1
                            pager[heading.split(" ")[-1].strip()]=fielddata
                            if counter==2:
                                counter=3
                                continue
                            if data[datas]!='' or True: 
                                if fielddata < 43:
                                    if fieldIndex >= len(fieldsdata):
                                        #fields = ET.SubElement(product, "field_"+str(fielddata))
                                        if not descriptionField.get(heading.split(" ")[-1].strip()) == None:
                                            fields= descriptionField.get(heading.split(" ")[-1].strip())
                                            A = descriptionMapper.get(heading.split(" ")[-1].strip())

                                        else : 
                                            A = ''
                                            descriptionMapper[heading.split(" ")[-1].strip()]=A
                                            fields = ET.SubElement(product, "description")
                                            descriptionField[heading.split(" ")[-1].strip()]=fields
                                        diss =True
                                    else :
                                        if(fieldsdata[fieldIndex]=='price_2'):
                                            datas=datas+1   
                                        fields = ET.SubElement(product,fieldsdata[fieldIndex] )#converter[fielddata])
                                        diss=False
                                        if(fieldsdata[fieldIndex]=='size_1'):
                                            datas=datas+1   
                                        fields = ET.SubElement(product,fieldsdata[fieldIndex] )#converter[fielddata])
                                        diss=False
                                    fieldIndex+=1

                                else:
                                    if not descriptionField.get(heading.split(" ")[-1].strip()) == None:
                                        fields= descriptionField.get(heading.split(" ")[-1].strip())
                                        A = descriptionMapper.get(heading.split(" ")[-1].strip())

                                    else : 
                                        A = ''
                                        descriptionMapper[heading.split(" ")[-1].strip()]=A
                                        fields = ET.SubElement(product, "description")
                                        descriptionField[heading.split(" ")[-1].strip()]=fields
                                    diss =True
                                tempF=fields
                                fielddata+=1
                                if(dictionary.item().get(data[datas].lower().strip())==None):
                                    if(len(data[datas].strip().split(' '))>1 ):
                                        K=data[datas].strip().split(" ")
                                        data[datas]=data[datas].strip()
                                        for l in range(len(K)):
                                            if(dictionary.item().get(K[l].lower().strip())==None):
                                                pass
                                            else: 
                                                K[l]=dictionary.item().get(K[l].lower().strip())[0]
                                        if fieldIndex!=1:
                                            tempss= str(" ".join(K)).strip()
                                        else :
                                            tempss =  data[datas];
                                    else :
                                        tempss =  data[datas];
                                else :
                                    if fieldIndex !=1:
                                        tempss =dictionary.item().get(data[datas].lower().strip())[0]
                                    else :
                                        tempss =  data[datas];
                                if not diss :
                                    fields.text = tempss
                                else :
                                    A=descriptionMapper[heading.split(" ")[-1].strip()]
                                    A=A + tempss;
                                    #print("ERROR  " +A)
                                    fields.text=A
                                    descriptionMapper[heading.split(" ")[-1].strip()]=A


        mydata = ET.tostring(products)
        self.save_xml_data(mydata,'xmlData')
    def save_xml_data(self,mydata,output_xml_file_name) :
        myfile = open("../Output/"+output_xml_file_name+".xml", "w")    #xmlDataAll
        myfile.write(mydata.decode('windows-1250')) 
        myfile.close()
        #sanitize


        path = '../Output/'+output_xml_file_name+'.xml'

        tree = ET.parse(path)
        root = tree.getroot()
        prev = None
        skufound=False
        for page in root:                     # iterate over pages
            elems_to_remove = []
            skufound = False
            for elem in page:
            
                if(elem.tag=='sku' and skufound):
                    elems_to_remove.append(elem);
                if(elem.tag=='sku'):
                    skufound=True;
                if not elem.text:
                    skufound=False
                    elems_to_remove.append(elem)
            print(elems_to_remove)
            for elem_to_remove in elems_to_remove:
                page.remove(elem_to_remove)

        for page in root:                     # iterate over pages
            elems_to_remove = []
            skufound = False
            for elem in page:
            
                if(elem.tag=='sku' and skufound):
                    elems_to_remove.append(elem);
                if(elem.tag=='sku'):
                    skufound=True;
                if not elem.text:
                    skufound=False
                    elems_to_remove.append(elem)
            print(elems_to_remove)
            for elem_to_remove in elems_to_remove:
                page.remove(elem_to_remove)
        # [...]
        tree.write("../Output/"+output_xml_file_name+"Sanitized.xml")


runner = SwisstimeXML()
runner.download_data('download','download1')
runner.process_data()