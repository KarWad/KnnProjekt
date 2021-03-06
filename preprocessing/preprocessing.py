#!/usr/local/python-2.7.5/bin/python

""" preprocessing.py
    ----------------
    @author = Ankai Lou
"""

###############################################################################
############# modules & libraries required for preprocessing text #############
###############################################################################

import os
from bs4 import BeautifulSoup

###############################################################################
###### modules for feature selection & feature vector dataset generation ######
###############################################################################
from document.document import Document
from lexicon.lexicon import Lexicon
from feature import feature

###############################################################################
############ function(s) for generating parse tree from .sgm files ############
###############################################################################

def __generate_tree(text):
    """ function: generate_tree
        -----------------------
        extract well-formatted tree from poorly-formatted sgml @text

        :param text: string representing sgml text for a set of articles
        :returns: parsetree @tree of the structured @text
    """
    return BeautifulSoup(text, "html.parser")

###############################################################################
########## function(s) for generating parse trees & document objects ##########
###############################################################################

def __parse_documents(datapath):
    """ function: parse_document
        ------------------------
        extract list of Document objects from token list

        :returns: list of document entities generated by generate_document()
    """
    documents = []
    pairs = dict([])
    # generate well-formatted document set for each file
    for file in os.listdir(datapath):
        # open 'reut2-XXX.sgm' file from /data directory
        path = os.path.join(datapath, file)
        data = open(path, 'r')
        text = data.read()
        data.close()
        tree = __generate_tree(text.lower())
        # separate segments & generate documents
        for reuter in tree.find_all("reuters"):
            document = Document(reuter)
            pairs[document] = reuter
        # generate tokenized word list for each document
        for document, reuter in pairs.iteritems():
            document.populate_word_list(reuter)
            documents.append(document)
        print ("Finished extracting information from file:", file)
    return documents

###############################################################################
################## main function - single point of execution ##################
###############################################################################

def begin(datapath='C:\Reuters'):
    """ function: begin
        ---------------
        sanitize input files into well-formatted, processable objects
        generate dataset (feature vectors, class labels) for .sgm file set:
    """
    # generate list of document objects for feature selection
    print('\nGenerating document objects. This may take some time...')
    documents = __parse_documents(datapath)
    # generate lexicon of unique words for feature reduction
    print('Document generation complete. Building lexicon...')
    lexicon = Lexicon(documents)
    # preprocessing phase finished. begin feature selection phase
    print('Lexicon generation complete. Generating feature vectors...')
    feature_vectors = feature.generate(documents, lexicon)
    print('Feature vector generation complete. Preprocessing phase complete!')
    return feature_vectors
