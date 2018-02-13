#!/usr/bin/python

# David Bamman
# 2/14/14
#
# Python port of train_hmm.pl:

# Noah A. Smith
# 2/21/08
# Code for maximum likelihood estimation of a bigram HMM from 
# column-formatted training data.

# Usage:  train_hmm.py tags text > hmm-file

# The training data should consist of one line per sequence, with
# states or symbols separated by whitespace and no trailing whitespace.
# The initial and final states should not be mentioned; they are 
# implied.  
# The output format is the HMM file format as described in viterbi.pl.

import sys,re
import math
from itertools import izip
from collections import defaultdict

vocab = {}
emissions = {} # count of (tag, token) pair
emissionsTotal = defaultdict(int) # dict to count each tag
transTri = {} # count of ([tm2tag, prevtag], tag) pair
transTotalTri = defaultdict(int) # dict to count each tag
transBi = {}
transTotalBi = defaultdict(int) # dict to count each tag
tagTotal = 0

TAG_FILE = sys.argv[1] # tag file
TOKEN_FILE = sys.argv[2] # token file
OOV_WORD = "OOV"
INIT_STATE = "init"
FINAL_STATE = "final"

# open file and process them
with open(TAG_FILE) as tagFile, open(TOKEN_FILE) as tokenFile:
	for tagString, tokenString in izip(tagFile, tokenFile):
		# get tag and token and zip them as pair
		tags = re.split("\s+", tagString.rstrip())
		tokens = re.split("\s+", tokenString.rstrip())
		pairs = zip(tags, tokens)

		prevtag = INIT_STATE
		tm2tag = INIT_STATE
		N = 0
		for (tag, token) in pairs:
			# For first time we see *any* word token, we pretend it is an OOV. 
			# This lets our model decide the rate at which new words of each POS-type should be expected 
			# (e.g., high for nouns, low for determiners).
			if token not in vocab: # new token?
				vocab[token] = 1
				token = OOV_WORD
			if tag not in emissions:
				emissions[tag] = defaultdict(int) # put it in emimission
			if prevtag not in transBi:
				transBi[prevtag] = defaultdict(int) # put it in transition
			if (tm2tag, prevtag) not in transTri:
				transTri[(tm2tag, prevtag)] = defaultdict(int)

			# increment the emission observation in dictionary
			emissions[tag][token] += 1
			emissionsTotal[tag] += 1

			# increment trigram transition observation in dictionary
			transTri[(tm2tag, prevtag)][tag] += 1
			transTotalTri[(tm2tag, prevtag)] += 1

			# increment bigram transition observation in dictionary
			transBi[prevtag][tag] += 1
			transTotalBi[prevtag] += 1

			# let prevtag be the current tag for next iteration
			if N > 1:
				tm2tag = prevtag
			prevtag = tag
			N += 1
			tagTotal += 1

		# don't forget the stop probability for each sentence
		if (tm2tag, prevtag) not in transTri:
			transTri[(tm2tag, prevtag)] = defaultdict(int)
		if prevtag not in transBi:
			transBi[prevtag] = defaultdict(int)
		transTri[(tm2tag, prevtag)][FINAL_STATE]+=1
		transTotalTri[(tm2tag, prevtag)]+=1
		transBi[prevtag][FINAL_STATE]+=1
		transTotalBi[prevtag]+=1

# applying deleted-interpolation
l1 = 0
l2 = 0
l3 = 0
for (tm2tag, prevtag) in transTri:
	for tag in transTri[(tm2tag, prevtag)]:
		# determine the probability of tri, bi, and unigram
		trigramCount = float(transTri[(tm2tag, prevtag)][tag])
		trigram = 0
		bigram = 0
		if transTotalTri[(tm2tag, prevtag)] > 1:
			trigram = (trigramCount-1) / ((transTotalTri[(tm2tag, prevtag)])-1)
		if transTotalBi[prevtag] > 1:
			bigram = (float(transBi[prevtag][tag])-1) / ((transTotalBi[prevtag])-1)
		unigram = (float(emissionsTotal[tag])-1) / (tagTotal-1)
		# find max and increment
		if trigram > bigram and trigram > unigram:
			l1 += trigramCount
		elif bigram > trigram and bigram > unigram:
			l2 += trigramCount
		elif unigram > trigram and unigram > bigram:
			l3 += trigramCount

# normalize l1, l2, l3
lamdaSum = l1 + l2 + l3
l1 = float(l1) / lamdaSum
l2 = float(l2) / lamdaSum
l3 = float(l3) / lamdaSum

# finding probability
for (tm2tag, prevtag) in transTri:
	for tag in transTri[(tm2tag, prevtag)]:
		trigramCount = float(transTri[(tm2tag, prevtag)][tag])
		trigram = (trigramCount) / ((transTotalTri[(tm2tag, prevtag)]))
		bigram = (float(transBi[prevtag][tag])) / ((transTotalBi[prevtag]))
		unigram = (float(emissionsTotal[tag])) / (tagTotal)
		probability = l1 * trigram + l2 * bigram + l3 * unigram
		# print "trans %s %s %s %s" % (tm2tag, prevtag, tag, probability)
		print "trans %s %s %s" % (prevtag, tag, probability)

for tag in emissions:
	for token in emissions[tag]:
		print "emit %s %s %s " % (tag, token, float(emissions[tag][token]) / (emissionsTotal[tag]))