import sys
import re
import math
import itertools
from pprint import pprint
from collections import defaultdict

INIT_STATE = 'init'
FINAL_STATE = 'final'
OOV_SYMBOL = 'OOV'
HMM_FILE = sys.argv[1] # hmm file
INPUT_FILE = sys.argv[2] # input file

tags = set()  # set of unique POS tags
trans = {}  # transisions
trans_bi = {}  # transisions
emit = {}  # emissions
voc = {}  # encountered words

# obtain emission and transition
with open(HMM_FILE) as hmmfile:
  for line in hmmfile.read().splitlines():
    # extract information for transition and emission
    trans_reg = 'trans\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
    emit_reg = 'emit\s+(\S+)\s+(\S+)\s+(\S+)'
    trans_match = re.match(trans_reg, line)
    emit_match = re.match(emit_reg, line)
    if trans_match:
      tm2, tm1, t, p, pbi = trans_match.groups()
      trans[(tm2, tm1, t)] = math.log(float(p))
      trans_bi[(tm1, t)] = math.log(float(pbi))
      tags.update([tm2, tm1, t])
    elif emit_match:
      tag, word, p = emit_match.groups()
      emit[(tag, word)] = math.log(float(p))
      voc[word] = 1
      tags.update([tag])

# viterbi algorithm
with open(INPUT_FILE) as inputfile:
  for line in inputfile.read().splitlines():
    line = line.split(' ')
    n = len(line)
    pi = {(0, INIT_STATE, INIT_STATE): 0.0}  # 0.0 because using logs
    bp = {}  # backpointers
    for k, word in enumerate(line):
      k = k + 1
      if word not in voc:
        word = OOV_SYMBOL
      for w, u, v in itertools.product(tags, tags, tags):
        if (v, word) in emit and (k-1, w, u) in pi:
          if (w, u, v) in trans:
            p = pi[(k-1, w, u)] + trans[(w, u, v)] + emit[(v, word)]
            if (k, u, v) not in pi or p > pi[(k, u, v)]:
              pi[(k, u, v)] = p
              bp[(k, u, v)] = w
          elif (u, v) in trans_bi:
            p = pi[(k-1, w, u)] + trans_bi[(u, v)] + emit[(v, word)]
            if (k, u, v) not in pi or p > pi[(k, u, v)]:
              pi[(k, u, v)] = p
              bp[(k, u, v)] = w
    goal = float('-inf')
    tag = INIT_STATE
    pretag = INIT_STATE
    foundgoal = False
    for u, v in itertools.product(tags, tags):
      p = float('-inf')
      if (n-1, u, v) in pi:
        if (u, v, FINAL_STATE) in trans:
          p = pi[(n-1, u, v)] + trans[(u, v, FINAL_STATE)]
        elif (v, FINAL_STATE) in trans_bi and (u, v) in trans_bi:
          p = pi[(n-1, u, v)] + trans_bi[(v, FINAL_STATE)]
        if not foundgoal or p > goal:
          goal = p
          tag = v
          pretag = u
          foundgoal = True
    if foundgoal:
      y = []
      y.append(tag)
      y.append(pretag)
      for k in xrange(n-2, 1, -1):
        y.append(bp[(k+1, pretag, tag)])
        temp = bp[(k+1, pretag, tag)]
        tag = pretag
        pretag = temp
      y.reverse()
      print ' '.join(y) + ' '
    else:
      print ' '.join([])