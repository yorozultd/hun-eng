# Hun-Eng Translator

>/Dictionary : It stores the converted dictionary and the script to create the dictionary file 
>
>/hun-eng : contains the original software 
>
>/XmlCreator : It contains the script to convert csv file to XML.
>
>/Output : It contains the output files.


# Scripts  

    dictmaker.py  to create a dictionary from the software 

    xmlcreator.py converts the csv file to the xml file 

# OUTPUT
	
	xmlData.xml contains the output
	
# Dictionary
	
	To read the dictionary goto /Dictionary
	
	> Open terminal there
	>python3
	>import numpy as np
	>a=np.load("dictionary.npy",allow_pickle=True)
	>a.item().get("WORD TO SEARCH IN THE DICTIONAY")

