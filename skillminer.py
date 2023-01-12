import sys
import logging
from cassis import *
import spacy
import os
from optparse import OptionParser
from datetime import datetime
import pickle

# option parser

parser = OptionParser()
parser.add_option("-t", "--terminologies", dest="terminologies",default="", action="store", type="string", help="A list of terminologies", metavar="terminologies")
parser.add_option("-p", "--path", dest="path",default="", action="store", type="string", help="The path for terminologies", metavar="path")
args = parser.parse_args()
parser.add_option("-l", "--log-file", dest="logfile", default="pipeline.log", action="store", type="string", help="The logfile", metavar="logfile")
parser.add_option("-d", "--debug",
                  action="store_true", dest="debug", default=False,
                  help="Debug mode")      
                  

(options, args) = parser.parse_args()

# Logging

ll = logging.INFO
if options.debug:
  ll = logging.DEBUG
logging.basicConfig(filename=options.logfile, encoding='utf-8', level=ll)

logging.info( "===== skillminer =======")


terminologies = str(options.terminologies).split(",")
path = str(options.path)

nlp = spacy.load("de_core_news_sm")
#path = os.getcwd()+"/"

c = ""
for line in sys.stdin:
    c = c + line

# Default Typesystem
typesystem=load_dkpro_core_typesystem()
# make cas out of stdin
cas = load_cas_from_xmi(c, typesystem=load_dkpro_core_typesystem())

# Get Token type
Token = typesystem.get_type("de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity")
# Create Spacy doc
logging.info("Building doc-object")
doc = nlp(cas.sofa_string)
logging.info("Loading terminologies ... ")
tokens = []
for t in terminologies:
    logging.info(path+t)
    loaded_matcher = pickle.load(open(path+t+".map", 'rb'))
    loaded_vocab = pickle.load(open(path+t+"-v.map", 'rb'))
    matches = loaded_matcher(doc)
    for match_id, start, end in matches:
        try:
            mapid = loaded_vocab[match_id]
        except:
            logging.debug("Error, no entry for id "+str(match_id))
            mapid = str(match_id)+"error"
        span = doc[start : end]
        span_char_start = span[0].idx
        span_char_end = span[-1].idx + len(span[-1].text)
        tokens.append (Token(begin=span_char_start, end=span_char_end, value=t+":"+str(mapid)) )
# Add NE

# xmiID=None, value=None, identifier=None, begin=0, end=4, type='bla'
#for ent in doc.ents:
    

for t in tokens:
    cas.add(t)

logging.info("===== skillminer ende =======")
    
print (cas.to_xmi())
