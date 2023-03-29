#! /usr/bin/python3

import sys
from os import listdir,system
import re

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize

import evaluator

## dictionary containig information from external knowledge resources
## WARNING: You may need to adjust the path to the resource files
external = {}
with open("resources/HSDB.txt") as h :
    for x in h.readlines() :
        external[x.strip().lower()] = "drug"
with open("resources/DrugBank.txt") as h :
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

#suffixes = ['azole', 'idine', 'amine', 'mycin']
suffixes_3 = ['vir']
suffixes_4 = ['afil', 'olol', 'pril', 'trel']
suffixes_5 = ['amine', 'asone', 'azole', 'bicin', 'bital', 'caine', 
              'fenac', 'idine', 'mycin', 'olone', 
              'parin', 'tinib', 'zepam', 'zolam','zosin']
suffixes_6 = ['dazole', 'dipine', 'lamide', 'nazole', 'pentin', 'profen', 'sartan', 
              'semide', 'setron', 'statin', 'tyline', 'vudine', 'zodone']
suffixes_7 = ['cycline', 'gliptin', 'iramine', 'mustine']
suffixes_8 = ['eprazole', 'floxacin', 'thiazide']
#suffixes_9 = ['glitazone']
groups = ['anti', 'non', 'drugs', 'block', 'steroid', 
          'anta', 'opio', 'beta', 'ants']


def classify_token(txt):

   # WARNING: This function must be extended with 
   #          more and better rules

    

   #GOOD RULES
   # 0
   if re.match('tinib', txt[-5:]): return "drug"
   elif re.match('floxacin', txt[-8:]): return "drug"
   elif re.match('eprazole', txt[-8:]): return "drug"
   elif re.match('mustine', txt[-7:]): return "drug"
   elif re.match('iramine', txt[-7:]): return "group"
   elif re.match('gliptin', txt[-7:]): return "drug"
   elif re.match('cycline', txt[-7:]): return "drug"
   elif re.match('zodone', txt[-6:]): return "drug"
   elif re.match('vudine', txt[-6:]): return "drug"
   elif re.match('tyline', txt[-6:]): return "drug"
   elif re.match('setron', txt[-6:]): return "drug"
   elif re.match('semide', txt[-6:]): return "drug"
   elif re.match('sartan', txt[-6:]): return "drug"
   elif re.match('profen', txt[-6:]): return "drug"
   elif re.match('pentin', txt[-6:]): return "drug"
   elif re.match('lamide', txt[-6:]): return "drug"
   elif re.match('dipine', txt[-6:]): return "drug"
   elif re.match('zolam', txt[-5:]): return "drug"
   elif re.match('zepam', txt[-5:]): return "drug"
   elif re.match('ipine', txt[-5:]): return "drug"
   elif re.match('fenac', txt[-5:]): return "drug"
   elif re.match('bital', txt[-5:]): return "drug"
   elif re.match('bicin', txt[-5:]): return "drug"
   elif re.match('trel', txt[-4:]): return "drug"
   elif re.match('pril', txt[-4:]): return "drug"
   elif re.match('irin', txt[-4:]): return "brand"
   elif re.match('[a-zA-Z]*orphan[a-zA-Z]*', txt): return "drug"
   elif re.match('idil', txt[-4:]): return "drug"
   elif re.match('[a-zA-Z]*etam[a-zA-Z]*', txt): return "drug"
   # 1
   elif re.match('nazole', txt[-6:]): return "drug"
   elif re.match('parin', txt[-5:]): return "drug"
   elif re.match('mycin', txt[-5:]): return "drug"
   elif re.match('olol', txt[-4:]): return "drug"
   elif re.match('warfarin', txt[-8:]): return "drug"
   elif re.match('oxin', txt[-4:]): return "drug"
   elif re.match('avir', txt[-4:]): return "drug"
   # 2
   elif re.match('opio', txt[:4]): return "group"
   elif re.match('dazole', txt[-6:]): return "drug"
   elif re.match('asone', txt[-5:]): return "drug"
   elif re.match('afil', txt[-4:]): return "drug"
   elif re.match('amide', txt[-5:]): return "drug"

   # 3
   elif txt[-5:] == "acids": return "group"
   # 4   
   elif re.match('zosin', txt[-5:]): return "drug"
   elif re.match('olone', txt[-5:]): return "drug"
   elif re.match('steroid', txt[:7]): return "group"
   # 6
   elif re.match('caine', txt[-5:]): return "drug"
   elif re.match('avir', txt[-4:]): return "drug"

   # 7
   elif re.match('vir', txt[-3:]): return "drug"
   # 8
   elif txt[-4:] == "oids": return "group"
   # 10
   #elif re.match('idine', txt[-5:]): return "drug"
   # 11
   elif re.match('statin', txt[-6:]): return "drug"
   # 12
   elif re.match('azole', txt[-5:]): return "drug"
   elif re.match('arin', txt[-5:]): return "drug"
   elif re.match('[a-zA-Z]*vita[a-zA-Z]*', txt): return "group"
   # 13
   elif re.match('thiazide', txt[-8:]): return "drug"
   # 15
   elif txt[-3:] == "ids": return "group"
   # 18
   elif re.match('anta', txt[:4]): return "group"
   # 20
   elif re.match('ole', txt[-3:]): return "drug"
   elif re.match('lin', txt[-3:]): return "drug"
   # 25
   elif re.match('beta', txt[:5]): return "group"
   # 28
   elif re.match('amine', txt[-5:]): return "drug"
   # 42
   elif re.match('ants', txt[-4:]): return "group"
   # 43
   elif re.match('[0-9][0-9]*-([a-z]*[A-Z]*)+', txt[:5]) is not None: return "drug_n"   

   # 85
   elif re.match('ics', txt[-3:]): return "group"
   # 103 
   #elif re.match('ine', txt[-3:]): return "drug"

   # 127
   elif re.match('anti', txt[:4]): return "group"
   elif txt.lower() in external : return external[txt.lower()]
   # 138
   #elif re.match('[a-zA-Z]*anti[a-zA-Z]*', txt): return "group"
   # 779
   #elif txt.isupper() : return "brand"


   #NIKO
   #if txt[-8:] in suffixes_8 : return "drug"
   #if txt[-7:] in suffixes_7 : return "drug"
   #if txt[-6:] in suffixes_6 : return "drug"
   #if txt[-5:] in suffixes_5 : return "drug"
   #if txt[-4:] in suffixes_4 : return "drug"
   #if txt[-3:] in suffixes_3 : return "drug"
   #if re.search('[a-z]*-[a-z]*', txt) != None : return "group"
   



   #if txt[-9:] in suffixes_9 : return "drug"
   #elif txt.isupper() and txt.find('-') == True : return "drug_n"
   #elif re.search('[0-9],[0-9]', txt) != None : return "drug_n"
        


   else : return "NONE"



   

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
    for (token_txt, token_start, token_end)  in tokens:
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
    outf = open(outfile, 'w')

    # process each file in input directory
    for f in listdir(datadir) :
      
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





















