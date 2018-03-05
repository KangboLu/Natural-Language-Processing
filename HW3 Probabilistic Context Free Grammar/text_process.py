import math
import sys

INPUT_FILE = sys.argv[1]

with open(INPUT_FILE) as inputfile:
  for line in inputfile.read().splitlines():
    start_index = 0
    for i in xrange(0, len(line)):
      if line[i] == ' ' and line[i+1] != ' ':
        start_index = i+1
        break 
    print line[start_index:len(line)]
