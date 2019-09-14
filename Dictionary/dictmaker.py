from bs4 import BeautifulSoup
import numpy as np
import progress
dictionary = {}
with open("../hun-eng/hun-eng.tei",'r') as tei :
    soup = BeautifulSoup(tei, 'lxml')
    a=soup.find_all("entry")               #getting all the entry data
    with open("readable.txt",'w') as f:
        f.write(soup.text)
    for i in a:                            #traversing throught the data
        hun=i.find("form").text[1:]       # get all the hun. I dont want the first character because it is - 
        eng=i.find_all("sense")           # get all the english synonyms 
        arr=[]
        for j in eng:                       #have to store all the english words in the array
            arr.append(j.text)          
        dictionary[hun]=arr;
        

np.save("dictionary",dictionary)
