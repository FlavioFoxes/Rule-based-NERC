#! /usr/bin/python3

import sys
from os import listdir,system
import re

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import evaluator

stopw = stopwords.words('english')
## dictionary containig information from external knowledge resources
## WARNING: You may need to adjust the path to the resource files
external = {}
with open("resources/HSDB.txt") as h :
# with open("C:/Users/nikop/Desktop/AHLT/labAHLT/resources/HSDB.txt") as h :
    for x in h.readlines() :
        external[x.strip().lower()] = "drug"
with open("resources/DrugBank.txt") as h :
# with open("C:/Users/nikop/Desktop/AHLT/labAHLT/resources/DrugBank.txt") as h :
    for x in h.readlines() :
        (n,t) = x.strip().lower().split("|")
        external[n] = t

        
## --------- tokenize sentence ----------- 
## -- Tokenize sentence, returning tokens and span offsets

def tokenize(txt):
    offset = 0
    tks = []
    for t in word_tokenize(txt):
        offset = txt.find(t, offset)
        tks.append((t, offset, offset+len(t)-1))
        offset += len(t)
    return tks

## -----------------------------------------------
## -- check if a token is a drug part, and of which type

suffixes_3 = ['mab', 'vir']
suffixes_4 = ['afil', 'cort', 'olol', 'pril', 'trel']
suffixes_5 = ['amine', 'asone', 'azole', 'bicin', 'bital', 'caine', 
              'cilin', 'fenac', 'idine', 'mycin', 'nacin', 'olone', 
              'onide', 'parin', 'terol', 'tinib', 'zepam', 'zolam',
              'zosin']
suffixes_6 = ['dazole', 'dipine', 'lamide', 'nazole', 'pentin', 'profen', 'ridone', 'sartan', 
              'semide', 'setron', 'statin', 'tretin', 'tyline', 'vudine', 'zodone']
suffixes_7 = ['cycline', 'dronate', 'gliptin', 'iramine', 'mustine', 'phyline', 'pramine', 'tadline']
suffixes_8 = ['eprazole', 'floxacin', 'oprazole', 'thiazide']
suffixes_9 = ['glitazone']
groups = ['anti', 'non', 'drugs', 'block', 'steroid', 
          'anta', 'opio', 'beta', 'ants']

def classify_token(txt):

    # WARNING: This function must be extended with 
    #          more and better rules

    if len(txt) > 3: 
        if txt[-3:] in suffixes_3 : return "drug"
        elif txt[-4:] in suffixes_4 : return "drug"
        elif txt[-5:] in suffixes_5 : return "drug"
        elif txt[-6:] in suffixes_6 : return "drug"
        elif txt[-7:] in suffixes_7 : return "drug"
        elif txt[-8:] in suffixes_8 : return "drug"
        elif txt[-9:] in suffixes_9 : return "drug"
        elif txt.isupper() and txt.find('-') == True : return "drug_n"
        elif re.search('[0-9],[0-9]', txt) != None : return "drug_n"
        elif re.search('[a-z]-[a-z]', txt) != None : return "group"
        else: 
            for gr in groups: 
                if re.search(gr, txt) != None: 
                    return "group"
                    break
        
        
                
        if txt.lower() in external : return external[txt.lower()]
        elif txt.isupper() : return "brand"

    return "NONE"

   

## --------- Entity extractor ----------- 
## -- Extract drug entities from given text and return them as
## -- a list of dictionaries with keys "offset", "text", and "type"

def extract_entities(stext) :

    # WARNING: This function must be extended to
    #          deal with multi-token entities.
    
    # tokenize text
    tokens = tokenize(stext)
    result = []
    # classify each token and decide whether it is an entity.
    i = 0
    for (token_txt, token_start, token_end) in tokens:
        drug_type = classify_token(token_txt)
        
        if drug_type != "NONE" :
            e = { "offset" : str(token_start)+"-"+str(token_end),
                  "text" : stext[token_start:token_end+1],
                  "type" : drug_type
                 }
            result.append(e)
                    
    return result

def extract_entities2(stext) :
    tokens = tokenize(stext)
    result = []
    i = 0
    while i < len(tokens):
        token_txt, token_start, token_end = tokens[i]
        drug_type0 = classify_token(token_txt)
        count = 1
        if drug_type0 != "NONE":
            e = { "offset" : str(token_start)+"-"+str(token_end),
                    "text" : stext[token_start:token_end+1],
                    "type" : drug_type0
                }
            while count < 5 and i+count < len(tokens)-1: 
                tmp_txt, tmp_start, tmp_end = tokens[i+count]
                tmp_type = classify_token(tmp_txt)
                if tmp_type != "NONE": 
                    token_txt += ' ' + tmp_txt
                    e = { "offset" : str(token_start)+"-"+str(tmp_end),
                        "text" : stext[token_start:tmp_end+1],
                        "type" : drug_type0
                        }
                else: 
                    break
                count += 1
            result.append(e) 
        i += count
    return result

      
## --------- main function ----------- 

def nerc(datadir, outfile) :
   
    # open file to write results
    outf = open(outfile, 'w+')

    # process each file in input directory
    for f in listdir(datadir) :
        if not f.endswith('.xml'):
            continue
        # parse XML file, obtaining a DOM tree
        tree = parse(datadir+"/"+f)
      
        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences :
            sid = s.attributes["id"].value   # get sentence id
            stext = s.attributes["text"].value   # get sentence text
            
            # extract entities in text
            entities = extract_entities2(stext)
         
            # print sentence entities in format requested for evaluation
            for e in entities :
                print(sid,
                      e["offset"],
                      e["text"],
                      e["type"],
                      sep = "|",
                      file=outf)
            
    outf.close()


   
## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir
## --

# directory with files to process
datadir = sys.argv[1]
outfile = sys.argv[2]

nerc(datadir,outfile)

evaluator.evaluate("NER", datadir, outfile)





















