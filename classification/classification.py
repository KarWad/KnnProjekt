#!/usr/local/python-2.7.5/bin/python

""" classification.py
    -----------------
    @author = Ankai Lou, Daniel Jaung
"""

###############################################################################
############ modules & libraries required for classifying articles ############
###############################################################################
from classification.classifier import knearestneighbor, knearestneighbor_balltree, decisiontree, bayesian
from crossvalidator.crossvalidator import CrossValidator
from classifier import *

###############################################################################
############################### global variables ##############################
###############################################################################

num_partitions = 5
num_neighbors = 3
epsilon = 0.0

###############################################################################
############################# list of classifiers #############################
###############################################################################

classifiers = [knearestneighbor.KNN(num_neighbors),
               knearestneighbor_balltree.BallTreeKNN(num_neighbors,epsilon),
               decisiontree.DecisionTree(epsilon),
               bayesian.Bayesian(epsilon)]

###############################################################################
################# strings representing classifier experiments #################
###############################################################################

fv_dataset_name = ["standard feature vector","pared feature vector"]

###############################################################################
############# function(s) for generating training & testing sets ##############
###############################################################################

def __filter_empty(feature_vectors):
    """ function: filter_empty
        ----------------------
        separate fv dataset into classified & unclassified data

        :param feature_vectors: dictionary representing feature vector dataset
        :returns: dictionaries of empty and non-empty feature vectors
    """
    empty = dict([])
    nonempty = dict([])
    for document, doc_dict in feature_vectors.iteritems():
        if len(feature_vectors[document].topics) == 0:
            empty[document] = feature_vectors[document]
        else:
            nonempty[document] = feature_vectors[document]
    return nonempty, empty

###############################################################################
################# main function for single-point-of-execution #################
###############################################################################

def begin(feature_vectors):
    """ function: begin
        ---------------
        use N classifiers on M feature vector datasets

        :param feature_vectors: standard dataset generated using tf-idf
    """
    # iterate across feature vector sets
    for i, dataset in enumerate(feature_vectors):
        fv, efv = __filter_empty(dataset)
        cross_validator = CrossValidator(fv,num_partitions)
        # iterate across classifiers
        for j, classifier in enumerate(classifiers):
            print ("\nExperiment:", classifier.name, "on", fv_dataset_name[i])
            cross_validator.classify(classifier)
