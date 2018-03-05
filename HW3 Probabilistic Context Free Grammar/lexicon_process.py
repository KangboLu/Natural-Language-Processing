import math
import sys

INPUT_FILE = sys.argv[1]

with open(INPUT_FILE) as inputfile:
  for line in inputfile.read().splitlines():
    start_index = 0
    end_index = 0
    for i in xrange(0, len(line)):
      if line[i] == '-' and line[i+1] == '>':
        start_index = i+3
        for j in xrange(start_index, len(line)):
          if line[j] == ' ':
            end_index = j-1
            break
        break
    print line[start_index:end_index+1]
