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

suffixes = ['azole', 'idine', 'amine', 'mycin']

def classify_token(txt):

   # WARNING: This function must be extended with 
   #          more and better rules

   #GOOD RULES
   ## 0
   if re.match('ipine', txt[-5:]): return "drug"
   elif re.match('[a-zA-Z]*orphan[a-zA-Z]*', txt): return "drug"
   elif re.match('[a-zA-Z]*etam[a-z]*', txt): return "drug"
   elif re.match('irin', txt[-4:]): return "brand"
   elif re.match('[a-zA-Z]*orphan[a-zA-Z]*', txt): return "drug"
   elif re.match('idil', txt[-4:]): return "drug"

   # 1
   elif re.match('warfarin', txt[-8:]): return "drug"
   elif re.match('oxin', txt[-5:]): return "drug"
   elif re.match('avir', txt[-4:]): return "drug"
   # 2
   elif re.match('amide', txt[-5:]): return "drug"
   # 3
   elif txt[-5:] == "acids": return "group"
   # 6
   elif re.match('avir', txt[-4:]): return "drug"

   # 8
   elif txt[-4:] == "oids": return "group"

   # 12
   elif re.match('arin', txt[-5:]): return "drug"
   elif re.match('[a-zA-Z]*vita[a-zA-Z]*', txt): return "group"
   # 15
   elif txt[-3:] == "ids": return "group"

   # 20
   elif re.match('ole', txt[-3:]): return "drug"
   elif re.match('lin', txt[-3:]): return "drug"
   # 25
   elif re.match('beta', txt[:5]): return "group"
   # 42
   elif re.match('ants', txt[-4:]): return "group"
   # 43
   elif re.match('[0-9][0-9]*\-([a-z]*[A-Z]*)+', txt[:5]) is not None: return "drug_n"   

   # 51
   elif txt[-5:] in suffixes : return "drug"
   # 85
   elif re.match('ics', txt[-3:]): return "group"
   # 103 
   elif re.match('ine', txt[-3:]): return "drug"

   # 138
   elif re.match('[a-zA-Z]*anti[a-zA-Z]*', txt): return "group"



   # 127
   #elif re.match('anti', txt[:4]): return "group"
   #elif txt.lower() in external : return external[txt.lower()]
   # 779
   #elif txt.isupper() : return "brand"
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
            entities = extract_entities(stext)
         
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





















