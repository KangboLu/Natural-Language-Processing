import sys
import re
import math
import itertools
from pprint import pprint
from collections import defaultdict

INIT_STATE = 'init'
FINAL_STATE = 'final'
OOV_SYMBOL = 'OOV'

hmmfile = 'my.hmm'
inputfile = 'ptb.22.txt'

tags = set()  # i.e. K in the slides, a set of unique POS tags
trans = {}  # transisions
emit = {}  # emissions
voc = {}  # encountered words

"""
This part parses the my.hmm file you have generated and obtain the transition and emission values.
"""
with open(hmmfile) as hmmfile:
  for line in hmmfile.read().splitlines():
    # extract information for transition and emission
    trans_reg = 'trans\s+(\S+)\s+(\S+)\s+(\S+)'
    emit_reg = 'emit\s+(\S+)\s+(\S+)\s+(\S+)'
    trans_match = re.match(trans_reg, line)
    emit_match = re.match(emit_reg, line)
    if trans_match:
      qq, q, p = trans_match.groups()
      trans[(qq, q)] = math.log(float(p))
      tags.update([qq, q])
    elif emit_match:
      q, w, p = emit_match.groups()
      emit[(q, w)] = math.log(float(p))
      voc[w] = 1
      tags.update([q])

"""
This part parses the file with the test sentences, and runs the sentence through the viterbi algorithm.
"""
with open(inputfile) as inputfile:
  for line in inputfile.read().splitlines():
    line = line.split(' ')
    # initialize pi.
    # i.e. set pi(0, *, *) = 1 from slides
    pi = {(0, INIT_STATE): 0.0}  # 0.0 because using logs
    bp = {}  # backpointers

    # for each word in sentence and their index
    for k, word in enumerate(line):
      k = k + 1
      if word not in voc:
        # change unseen words into OOV, since OOV is assigned a score in train_hmm. This will give these unseen words a score instead of a mismatch.
        word = OOV_SYMBOL
      for u, v in itertools.product(tags, tags):  # python nested for loop
        # i.e. the first bullet point from the slides.
        # Calculate the scores (p) for each possible combinations of (u, v)
        if (v, u) in trans and (u, word) in emit and (k - 1, v) in pi:
          p = pi[(k - 1, v)] + trans[(v, u)] + emit[(u, word)]
          if (k, u) not in pi or p > pi[(k, u)]:
            # here, fine the max of all the calculated p, update it in the pi dictionary
            pi[(k, u)] = p
            # also keeping track of the backpointer
            bp[(k, u)] = v

    # second bullet point from the slides.
    # Taking the case for the last word. Find the corrsponding POS tag for that word so we can then start the backtracing.
    foundgoal = False
    goal = float('-inf')
    tag = INIT_STATE
    for v in tags:
      # You want to try each (tag, FINAL_STATE) pair for the last word and find which one has max p. That will be the tag you choose.
      if (v, FINAL_STATE) in trans and (len(line), v) in pi:
        p = pi[(len(line), v)] + trans[(v, FINAL_STATE)]
        if not foundgoal or p > goal:
          # finding tag with max p
          goal = p
          foundgoal = True
          tag = v

    # if pi is greater than previous recorded pi
    if foundgoal:
      # y is the sequence of final chosen tags
      y = []
      for i in xrange(len(line), 1, -1):  # counting from the last word
        # bp[(i, tag)] gives you the tag for word[i - 1].
        # we use that and traces through the tags in the sentence.
        y.append(bp[(i, tag)])
        tag = bp[(i, tag)]

      # y is appened last tag first. Reverse it.
      y.reverse()
      # print the final output
      print ' '.join(y)
    else:
      # append blank line if something fails so that each sentence is still printed on the correct line.
      print '\n'